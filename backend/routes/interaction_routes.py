"""
Drug Interaction Analysis Routes.
"""
from flask import Blueprint, request, jsonify
from services.interaction_service import find_interactions_for_drugs
from database.db import execute_db
from config import Config

interaction_bp = Blueprint("interaction_bp", __name__)

@interaction_bp.route("/check", methods=["POST"])
def check_interactions():
    """Checks interactions between a list of 2 or more medicines."""
    data = request.get_json() or {}
    medicines = data.get("medicines", [])

    if not isinstance(medicines, list) or len(medicines) < 2:
        return jsonify({
            "success": False,
            "message": "Please provide an array of at least 2 medicine names in 'medicines'."
        }), 400

    report = find_interactions_for_drugs(medicines)

    # Save to search history
    drugs_str = ", ".join(report["drugs_checked"])
    execute_db(
        "INSERT INTO search_history (query, search_type, result_summary, matched_medicine) VALUES (?, ?, ?, ?)",
        (f"Interactions: {drugs_str}", "interaction", f"Found {report['total_interactions']} interaction(s). Risk: {report['risk_level']}", drugs_str)
    )

    return jsonify({
        "success": True,
        "data": report,
        "disclaimer": Config.SAFETY_DISCLAIMER
    })

@interaction_bp.route("/common", methods=["GET"])
def get_common_test_pairs():
    """Returns sample pre-defined drug combinations for one-click testing."""
    test_combinations = [
        {
            "title": "Aspirin + Warfarin (Blood Thinners)",
            "medicines": ["Aspirin", "Warfarin"],
            "expected_severity": "Major",
            "clinical_concern": "Synergistic bleeding hazard"
        },
        {
            "title": "Ibuprofen + Lisinopril (NSAID + Blood Pressure)",
            "medicines": ["Ibuprofen", "Lisinopril"],
            "expected_severity": "Moderate",
            "clinical_concern": "Decreased blood pressure control & renal strain"
        },
        {
            "title": "Metformin + Alcohol (Antidiabetic Warning)",
            "medicines": ["Metformin", "Alcohol"],
            "expected_severity": "Major",
            "clinical_concern": "Elevated lactic acidosis risk"
        },
        {
            "title": "Omeprazole + Clopidogrel (Acid Reducer + Plavix)",
            "medicines": ["Omeprazole", "Clopidogrel"],
            "expected_severity": "Major",
            "clinical_concern": "Decreased antiplatelet efficacy"
        },
        {
            "title": "Sertraline + Tramadol (Antidepressant + Painkiller)",
            "medicines": ["Sertraline", "Tramadol"],
            "expected_severity": "Major",
            "clinical_concern": "Serotonin Syndrome risk"
        },
        {
            "title": "Paracetamol + Cetirizine (Pain + Allergy)",
            "medicines": ["Paracetamol", "Cetirizine"],
            "expected_severity": "Safe / Minor",
            "clinical_concern": "Common OTC combination (Safe)"
        }
    ]
    return jsonify({"success": True, "common_combinations": test_combinations})
