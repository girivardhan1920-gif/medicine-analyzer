"""
AI Medicine Analyzer - Flask REST API Backend
"""
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = str(Path(__file__).resolve().parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database.db import init_db, query_db
from database.seed_data import seed_database
from routes.medicine_routes import medicine_bp
from routes.interaction_routes import interaction_bp
from routes.chat_routes import chat_bp
from routes.history_routes import history_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("ai_medicine_analyzer")

def create_app():
    """Application factory for Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable Cross-Origin Resource Sharing
    CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"])

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Register API Blueprints
    app.register_blueprint(medicine_bp, url_prefix="/api/medicine")
    app.register_blueprint(interaction_bp, url_prefix="/api/interactions")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(history_bp, url_prefix="/api/history")

    # Initialize and Seed Database if needed
    with app.app_context():
        try:
            init_db()
            # Check if medicines exist, if not seed
            count = query_db("SELECT COUNT(*) as c FROM medicines", one=True)
            if not count or count["c"] == 0:
                logger.info("Initializing database with 50+ medicines and interaction rules...")
                seed_database()
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    # Root URL
    @app.route("/", methods=["GET"])
    def root():
        """Root endpoint returning service status and available routes."""
        return jsonify({
            "service": "AI Medicine Analyzer Backend REST API",
            "status": "online",
            "version": "1.0.0",
            "health_check": "/api/health",
            "endpoints": {
                "health": "/api/health",
                "stats": "/api/stats",
                "search": "/api/medicine/search?q={name}",
                "interactions": "/api/interactions/check",
                "chat": "/api/chat",
                "history": "/api/history"
            },
            "message": "Backend REST API is operational."
        })

    # Health Check API
    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint for verifying backend status."""
        try:
            med_count = query_db("SELECT COUNT(*) as c FROM medicines", one=True)["c"]
            inter_count = query_db("SELECT COUNT(*) as c FROM drug_interactions", one=True)["c"]
            db_status = "Healthy"
        except Exception as e:
            med_count = 0
            inter_count = 0
            db_status = f"Degraded ({e})"

        return jsonify({
            "status": "online",
            "service": "AI Medicine Analyzer API",
            "version": "1.0.0",
            "database": db_status,
            "total_medicines_indexed": med_count,
            "total_interaction_rules": inter_count,
            "gemini_ai_configured": bool(Config.GEMINI_API_KEY),
            "safety_disclaimer": Config.SAFETY_DISCLAIMER
        })

    # Dashboard Stats API
    @app.route("/api/stats", methods=["GET"])
    def get_dashboard_stats():
        """Returns statistics for the dashboard overview cards."""
        try:
            total_meds = query_db("SELECT COUNT(*) as c FROM medicines", one=True)["c"]
            total_interactions = query_db("SELECT COUNT(*) as c FROM drug_interactions", one=True)["c"]
            total_searches = query_db("SELECT COUNT(*) as c FROM search_history", one=True)["c"]
            categories = query_db("SELECT COUNT(DISTINCT category) as c FROM medicines", one=True)["c"]
        except Exception:
            total_meds, total_interactions, total_searches, categories = 50, 40, 0, 8

        return jsonify({
            "success": True,
            "stats": {
                "total_medicines": total_meds,
                "known_interactions": total_interactions,
                "total_queries_processed": total_searches,
                "therapeutic_categories": categories
            }
        })

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Endpoint or resource not found.", "code": 404}), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return jsonify({"success": False, "error": "File size exceeds 16MB limit.", "code": 413}), 413

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"success": False, "error": "Internal server error occurred.", "code": 500}), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting AI Medicine Analyzer Backend on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
