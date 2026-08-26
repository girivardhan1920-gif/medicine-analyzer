"""
Search History and Audit Routes.
"""
from flask import Blueprint, request, jsonify
from database.db import query_db, execute_db

history_bp = Blueprint("history_bp", __name__)

@history_bp.route("", methods=["GET"])
def get_history():
    """Retrieve recent medicine and interaction searches."""
    limit = request.args.get("limit", 50, type=int)
    search_type = request.args.get("type", "").strip()

    if search_type:
        rows = query_db(
            "SELECT * FROM search_history WHERE search_type = ? ORDER BY created_at DESC LIMIT ?",
            (search_type, limit)
        )
    else:
        rows = query_db(
            "SELECT * FROM search_history ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )

    # Summary statistics for dashboard
    total_searches = query_db("SELECT COUNT(*) as c FROM search_history", one=True)["c"]
    text_searches = query_db("SELECT COUNT(*) as c FROM search_history WHERE search_type='text'", one=True)["c"]
    image_searches = query_db("SELECT COUNT(*) as c FROM search_history WHERE search_type='image_ocr'", one=True)["c"]
    interaction_checks = query_db("SELECT COUNT(*) as c FROM search_history WHERE search_type='interaction'", one=True)["c"]

    return jsonify({
        "success": True,
        "history": rows,
        "stats": {
            "total_searches": total_searches,
            "text_searches": text_searches,
            "image_searches": image_searches,
            "interaction_checks": interaction_checks
        }
    })

@history_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_history_item(item_id):
    """Delete a single history entry."""
    execute_db("DELETE FROM search_history WHERE id = ?", (item_id,))
    return jsonify({"success": True, "message": f"History item {item_id} deleted."})

@history_bp.route("/clear", methods=["POST"])
def clear_all_history():
    """Clear entire search history."""
    execute_db("DELETE FROM search_history")
    return jsonify({"success": True, "message": "Search history cleared."})
