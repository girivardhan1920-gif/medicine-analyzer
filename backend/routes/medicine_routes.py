"""
Medicine Information, Search, Analysis & Image OCR Routes.
"""
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from database.db import query_db, execute_db
from services.fda_service import query_openfda_by_name
from services.ocr_service import process_medicine_image
from services.ai_service import simplify_medical_info
from config import Config

medicine_bp = Blueprint("medicine_bp", __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@medicine_bp.route("/search", methods=["GET"])
def search_medicines():
    """Autocomplete and keyword search across medicine names, generic names, and brands."""
    q = request.args.get("q", "").strip()
    if not q:
        # Return top 15 medicines
        rows = query_db("SELECT id, name, generic_name, brand_names, category FROM medicines ORDER BY name ASC LIMIT 15")
        return jsonify({"success": True, "results": rows, "count": len(rows)})

    search_term = f"%{q}%"
    sql = """
        SELECT id, name, generic_name, brand_names, category, common_uses
        FROM medicines
        WHERE name LIKE ? OR generic_name LIKE ? OR brand_names LIKE ? OR category LIKE ?
        ORDER BY 
            CASE 
                WHEN LOWER(name) = LOWER(?) THEN 1
                WHEN name LIKE ? THEN 2
                ELSE 3
            END,
            name ASC
        LIMIT 20
    """
    rows = query_db(sql, (search_term, search_term, search_term, search_term, q, f"{q}%"))
    return jsonify({"success": True, "query": q, "results": rows, "count": len(rows)})

@medicine_bp.route("/<name>", methods=["GET"])
def get_medicine_by_name(name):
    """Retrieve full details of a specific medicine from local DB or OpenFDA."""
    clean_name = name.strip()
    # 1. Check local DB
    med = query_db(
        "SELECT * FROM medicines WHERE LOWER(name) = LOWER(?) OR LOWER(generic_name) = LOWER(?)",
        (clean_name, clean_name),
        one=True
    )
    
    if not med:
        # Partial match
        med = query_db(
            "SELECT * FROM medicines WHERE name LIKE ? OR generic_name LIKE ? LIMIT 1",
            (f"%{clean_name}%", f"%{clean_name}%"),
            one=True
        )

    # 2. Fallback to OpenFDA live lookup if not in local DB
    source = "Local Verified Database"
    if not med:
        fda_data = query_openfda_by_name(clean_name)
        if fda_data:
            med = fda_data
            source = fda_data.get("source", "OpenFDA")

    if not med:
        return jsonify({
            "success": False,
            "message": f"Information not available for '{clean_name}'. Please verify the spelling.",
            "data": None
        }), 404

    # Generate AI layman breakdown
    ai_breakdown = simplify_medical_info(med)

    return jsonify({
        "success": True,
        "source": source,
        "data": med,
        "ai_explanation": ai_breakdown,
        "disclaimer": Config.SAFETY_DISCLAIMER
    })

@medicine_bp.route("/analyze", methods=["POST"])
def analyze_medicine():
    """Analyzes a medicine query, fetches data, generates AI explanation, and logs to history."""
    data = request.get_json() or {}
    medicine_name = data.get("medicine_name", "").strip()

    if not medicine_name:
        return jsonify({"success": False, "message": "Medicine name is required."}), 400

    # Retrieve medicine details
    med = query_db(
        "SELECT * FROM medicines WHERE LOWER(name) = LOWER(?) OR LOWER(generic_name) = LOWER(?)",
        (medicine_name, medicine_name),
        one=True
    )

    if not med:
        med = query_db(
            "SELECT * FROM medicines WHERE name LIKE ? OR generic_name LIKE ? OR brand_names LIKE ? LIMIT 1",
            (f"%{medicine_name}%", f"%{medicine_name}%", f"%{medicine_name}%"),
            one=True
        )

    source = "Local Verified Database"
    if not med:
        fda_res = query_openfda_by_name(medicine_name)
        if fda_res:
            med = fda_res
            source = fda_res.get("source", "OpenFDA")

    if not med:
        return jsonify({
            "success": False,
            "message": f"Could not find verified medical information for '{medicine_name}'.",
            "medicine_name": medicine_name,
            "disclaimer": Config.SAFETY_DISCLAIMER
        }), 404

    # AI simplification
    ai_summary = simplify_medical_info(med)

    # Save to search history
    execute_db(
        "INSERT INTO search_history (query, search_type, result_summary, matched_medicine) VALUES (?, ?, ?, ?)",
        (medicine_name, "text", f"Analyzed {med['name']} ({med['category']})", med["name"])
    )

    return jsonify({
        "success": True,
        "source": source,
        "medicine": med,
        "ai_analysis": ai_summary,
        "disclaimer": Config.SAFETY_DISCLAIMER
    })

@medicine_bp.route("/image", methods=["POST"])
def analyze_medicine_image():
    """Uploads medicine packaging photo, extracts text via OCR/Vision, identifies drug, and analyzes it."""
    if 'image' not in request.files:
        return jsonify({"success": False, "message": "No image file provided in request."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "message": "Empty file uploaded."}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Invalid image format. Allowed: PNG, JPG, JPEG, WEBP."}), 400

    filename = secure_filename(file.filename)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    saved_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(saved_path)

    # Run OCR Pipeline
    ocr_result = process_medicine_image(saved_path, filename)
    detected_name = ocr_result["detected_name"]

    # Match detected name against database
    med = None
    if detected_name != "Unknown Medicine":
        med = query_db(
            "SELECT * FROM medicines WHERE LOWER(name) = LOWER(?) OR LOWER(generic_name) = LOWER(?)",
            (detected_name, detected_name),
            one=True
        )
        if not med:
            med = query_db(
                "SELECT * FROM medicines WHERE name LIKE ? OR generic_name LIKE ? LIMIT 1",
                (f"%{detected_name}%", f"%{detected_name}%"),
                one=True
            )
        if not med:
            med = query_openfda_by_name(detected_name)

    ai_summary = simplify_medical_info(med) if med else None

    # Log to search history
    execute_db(
        "INSERT INTO search_history (query, search_type, result_summary, matched_medicine) VALUES (?, ?, ?, ?)",
        (f"Image: {filename}", "image_ocr", f"OCR detected '{detected_name}' via {ocr_result['method']}", detected_name if med else "Unidentified")
    )

    return jsonify({
        "success": True,
        "ocr_details": ocr_result,
        "matched": bool(med),
        "medicine": med,
        "ai_analysis": ai_summary,
        "disclaimer": Config.SAFETY_DISCLAIMER
    })

@medicine_bp.route("/categories", methods=["GET"])
def get_categories():
    """Returns list of categories with drug counts for easy browsing."""
    rows = query_db("SELECT category, COUNT(*) as count FROM medicines GROUP BY category ORDER BY count DESC")
    return jsonify({"success": True, "categories": rows})

@medicine_bp.route("/featured", methods=["GET"])
def get_featured_medicines():
    """Returns featured medicines for one-click quick analysis."""
    featured_names = ["Paracetamol", "Amoxicillin", "Atorvastatin", "Metformin", "Omeprazole", "Cetirizine", "Ibuprofen", "Amlodipine"]
    placeholders = ",".join(["?"] * len(featured_names))
    rows = query_db(f"SELECT * FROM medicines WHERE name IN ({placeholders})", featured_names)
    return jsonify({"success": True, "featured": rows})
