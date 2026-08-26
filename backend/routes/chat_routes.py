"""
AI Medical Chatbot Assistant Routes.
"""
from flask import Blueprint, request, jsonify
from services.ai_service import handle_chat_query
from database.db import execute_db, query_db
from config import Config

chat_bp = Blueprint("chat_bp", __name__)

@chat_bp.route("", methods=["POST"])
def chat():
    """Context-aware grounded AI chat endpoint with safety guardrails."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "default-session")

    if not message:
        return jsonify({"success": False, "message": "Message content is required."}), 400

    response = handle_chat_query(message, session_id)

    # Save to chat_logs
    execute_db(
        "INSERT INTO chat_logs (session_id, user_message, ai_response, safety_flag) VALUES (?, ?, ?, ?)",
        (session_id, message, response["reply"], response.get("safety_flag", 0))
    )

    return jsonify({
        "success": True,
        "reply": response["reply"],
        "safety_flag": response.get("safety_flag", 0),
        "matched_drug": response.get("matched_drug"),
        "disclaimer": Config.SAFETY_DISCLAIMER
    })

@chat_bp.route("/sample-prompts", methods=["GET"])
def sample_prompts():
    """Returns useful starter questions for demonstrating the AI chatbot."""
    prompts = [
        "What are the main side effects of Metformin?",
        "Can I take Ibuprofen with Lisinopril?",
        "Why must Levothyroxine be taken on an empty stomach?",
        "What should I do if I miss a dose of Amoxicillin?",
        "What are the warnings associated with long-term Omeprazole use?",
        "Is Paracetamol safe to take with food?"
    ]
    return jsonify({"success": True, "prompts": prompts})
