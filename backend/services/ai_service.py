"""
AI Medical Explanation & Assistant Service.
Grounds all summaries and chatbot responses on verified pharmaceutical databases with strict guardrails.
"""
import re
import logging
from config import Config
from database.db import query_db

logger = logging.getLogger(__name__)

SAFETY_GUARDRAILS = (
    "\n\n⚠️ Disclaimer: This AI analysis is for informational & educational purposes only. "
    "It is NOT a medical diagnosis, prescription, or clinical recommendation. "
    "Always consult a licensed doctor or pharmacist before starting, stopping, or changing any medication."
)

def simplify_medical_info(medicine_dict):
    """
    Generates a simple, layman-friendly AI summary of a medicine without inventing facts.
    """
    if not medicine_dict:
        return {"summary": "Information not available in verified records.", "key_takeaways": []}

    name = medicine_dict.get("name", "This medicine")
    generic = medicine_dict.get("generic_name", "")
    category = medicine_dict.get("category", "medication")
    uses = medicine_dict.get("common_uses", "")
    precautions = medicine_dict.get("general_precautions", "")
    side_effects = medicine_dict.get("common_side_effects", "")
    warnings = medicine_dict.get("warnings", "")
    storage = medicine_dict.get("storage_info", "")

    # If Gemini API Key is available, prompt Gemini with strict grounding
    if Config.GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = (
                f"You are a medical education AI assistant. Summarize the following verified drug details "
                f"into simple, clear language for a general reader. "
                f"DO NOT add unverified facts. Strictly avoid prescribing or diagnosing.\n\n"
                f"Medicine: {name} (Generic: {generic})\n"
                f"Category: {category}\n"
                f"Uses: {uses}\n"
                f"Precautions: {precautions}\n"
                f"Side Effects: {side_effects}\n"
                f"Warnings: {warnings}\n"
                f"Storage: {storage}\n\n"
                f"Output format:\n"
                f"1. Brief 2-sentence layman summary\n"
                f"2. Three bullet points for 'Important Things to Remember'"
            )
            response = model.generate_content(prompt)
            if response and response.text:
                return {
                    "summary": response.text.strip(),
                    "grounded_on": "Google Gemini 1.5 Flash + Verified Drug Database",
                    "disclaimer": Config.SAFETY_DISCLAIMER
                }
        except Exception as e:
            logger.warning(f"Gemini generation fallback to rule engine: {e}")

    # High-quality deterministic rule-based medical simplifier
    simple_summary = (
        f"{name} ({generic}) belongs to the class of {category.lower()}. "
        f"It is primarily utilized for {uses.lower().rstrip('.')}."
    )

    takeaways = [
        f"Primary Purpose: {uses}",
        f"Key Safety Caution: {precautions}",
        f"Storage: {storage}"
    ]

    return {
        "summary": simple_summary,
        "key_takeaways": takeaways,
        "grounded_on": "Verified Pharmaceutical Database & OpenFDA Records",
        "disclaimer": Config.SAFETY_DISCLAIMER
    }

def handle_chat_query(user_message, session_id=None):
    """
    Context-aware Medical Chatbot response grounded in knowledge base with safety guardrails.
    """
    user_msg_clean = user_message.strip()
    user_lower = user_msg_clean.lower()

    # Safety Guardrail: Detect diagnosis or emergency keywords
    emergency_keywords = ["overdose", "chest pain", "can't breathe", "cannot breathe", "suicide", "bleeding profusely", "unconscious"]
    for kw in emergency_keywords:
        if kw in user_lower:
            return {
                "reply": (
                    "🚨 **EMERGENCY NOTICE**: If you or someone else is experiencing severe symptoms, chest pain, "
                    "breathing difficulty, or suspected drug poisoning/overdose, please call emergency services (e.g. 911, 112, 108) "
                    "or visit the nearest emergency room immediately." + SAFETY_GUARDRAILS
                ),
                "safety_flag": 1
            }

    # Safety Guardrail: Detect direct diagnostic requests
    diagnostic_queries = ["do i have", "diagnose me", "what disease do i have", "prescribe me", "how much should i take to cure"]
    for dq in diagnostic_queries:
        if dq in user_lower:
            return {
                "reply": (
                    "I cannot diagnose diseases or determine medical conditions based on symptoms. "
                    "Only a qualified physician can evaluate your clinical history, perform physical exams, and diagnose conditions. "
                    "I can, however, provide general educational information about specific medicines, their mechanisms, and known interactions." + SAFETY_GUARDRAILS
                ),
                "safety_flag": 1
            }

    # Search local database for mentioned medicines to ground the response
    all_meds = query_db("SELECT name, generic_name, category, common_uses, general_precautions, common_side_effects, warnings, storage_info FROM medicines")
    found_med = None
    for med in all_meds:
        if med["name"].lower() in user_lower or med["generic_name"].lower() in user_lower:
            found_med = med
            break

    # If Gemini API key is available and configured
    if Config.GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            grounding_context = ""
            if found_med:
                grounding_context = (
                    f"Ground your answer strictly on this verified medical profile:\n"
                    f"Drug: {found_med['name']} ({found_med['generic_name']})\n"
                    f"Class: {found_med['category']}\n"
                    f"Uses: {found_med['common_uses']}\n"
                    f"Precautions: {found_med['general_precautions']}\n"
                    f"Side Effects: {found_med['common_side_effects']}\n"
                    f"Warnings: {found_med['warnings']}\n"
                    f"Storage: {found_med['storage_info']}\n"
                )

            system_instructions = (
                "You are an AI Pharmacist Education Assistant. Rules:\n"
                "1. Answer clearly, accurately, and politely in simple language.\n"
                "2. Never hallucinate facts.\n"
                "3. Never diagnose a user or prescribe medicine dosages.\n"
                "4. Always recommend consulting a doctor or pharmacist for clinical decisions.\n"
                "5. If information is not in the grounding context or widely established medical literature, state 'Information not available in verified records'."
            )
            
            full_prompt = f"{system_instructions}\n\n{grounding_context}\n\nUser Question: {user_msg_clean}"
            response = model.generate_content(full_prompt)
            if response and response.text:
                return {
                    "reply": response.text.strip() + SAFETY_GUARDRAILS,
                    "safety_flag": 0,
                    "matched_drug": found_med["name"] if found_med else None
                }
        except Exception as e:
            logger.warning(f"Gemini chat fallback: {e}")

    # High-quality grounded fallback engine
    if found_med:
        name = found_med["name"]
        generic = found_med["generic_name"]
        category = found_med["category"]
        
        if "side effect" in user_lower or "adverse" in user_lower:
            reply = f"**Common Side Effects of {name} ({generic})**:\n{found_med['common_side_effects']}\n\n**Important Precautions**:\n{found_med['general_precautions']}"
        elif "use" in user_lower or "for what" in user_lower or "indication" in user_lower or "help with" in user_lower:
            reply = f"**Primary Medical Uses for {name} ({generic})**:\n{found_med['common_uses']}\n\nIt belongs to the **{category}** drug category."
        elif "warning" in user_lower or "danger" in user_lower or "risk" in user_lower:
            reply = f"**Clinical Warnings for {name}**:\n{found_med['warnings']}\n\n**Precautions**:\n{found_med['general_precautions']}"
        elif "store" in user_lower or "keep" in user_lower:
            reply = f"**Storage Guidelines for {name}**:\n{found_med['storage_info']}"
        else:
            reply = (
                f"**{name} ({generic}) Overview**:\n\n"
                f"• **Category**: {category}\n"
                f"• **Common Uses**: {found_med['common_uses']}\n"
                f"• **Key Precautions**: {found_med['general_precautions']}\n"
                f"• **Common Side Effects**: {found_med['common_side_effects']}\n"
                f"• **Storage**: {found_med['storage_info']}"
            )
        return {
            "reply": reply + SAFETY_GUARDRAILS,
            "safety_flag": 0,
            "matched_drug": name
        }

    # General questions
    if "hello" in user_lower or "hi" in user_lower or "hey" in user_lower:
        return {
            "reply": (
                "Hello! I am your **AI Medicine Assistant**. "
                "You can ask me about any medicine's generic name, primary uses, common side effects, "
                "storage instructions, or drug interactions. "
                "How can I assist your educational research today?" + SAFETY_GUARDRAILS
            ),
            "safety_flag": 0
        }

    return {
        "reply": (
            f"Information not available in verified records for '{user_msg_clean}'. "
            "Please check the spelling of the medicine name, or try searching for common medications like "
            "Paracetamol, Ibuprofen, Amoxicillin, Metformin, Lisinopril, Omeprazole, or Cetirizine." + SAFETY_GUARDRAILS
        ),
        "safety_flag": 0
    }
