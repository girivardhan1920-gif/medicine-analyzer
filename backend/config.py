import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for backend
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

class Config:
    """Application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "ai-medicine-analyzer-secret-key-2026")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "database" / "medicine_analyzer.db"))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}
    
    # Gemini AI configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # OpenFDA API base
    OPENFDA_API_BASE = "https://api.fda.gov/drug"
    
    # Safety notice template
    SAFETY_DISCLAIMER = (
        "EDUCATIONAL USE ONLY: This information is for educational purposes and is not a substitute "
        "for professional medical advice, diagnosis, or treatment. Always consult a qualified physician "
        "or pharmacist regarding any medications or health conditions."
    )
