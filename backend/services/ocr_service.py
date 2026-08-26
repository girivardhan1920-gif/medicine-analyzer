"""
OCR and Package Recognition Service.
Extracts text from uploaded medicine packaging images using image preprocessing,
Tesseract OCR (if available), Google Gemini Vision (if configured), and regex/fuzzy matcher.
"""
import os
import re
import logging
from PIL import Image, ImageEnhance, ImageFilter
from config import Config

logger = logging.getLogger(__name__)

# List of known common medicine keywords for pattern matching
KNOWN_MEDS = [
    "paracetamol", "acetaminophen", "tylenol", "panadol", "crocin", "dolo",
    "ibuprofen", "advil", "motrin", "brufen", "nurofen",
    "aspirin", "ecosprin", "disprin", "naproxen", "aleve", "tramadol",
    "amoxicillin", "amoxil", "augmentin", "azithromycin", "zithromax", "z-pak",
    "ciprofloxacin", "cipro", "doxycycline", "cephalexin", "keflex",
    "amlodipine", "norvasc", "lisinopril", "zestril", "losartan", "cozaar",
    "metoprolol", "toprol", "atorvastatin", "lipitor", "rosuvastatin", "crestor",
    "hydrochlorothiazide", "furosemide", "lasix", "warfarin", "coumadin", "clopidogrel", "plavix",
    "metformin", "glucophage", "glimepiride", "amaryl", "sitagliptin", "januvia",
    "levothyroxine", "synthroid", "omeprazole", "prilosec", "pantoprazole", "protonix",
    "famotidine", "pepcid", "ondansetron", "zofran", "domperidone",
    "cetirizine", "zyrtec", "montelukast", "singulair", "salbutamol", "albuterol", "ventolin",
    "budesonide", "fexofenadine", "allegra",
    "alprazolam", "xanax", "sertraline", "zoloft", "escitalopram", "lexapro",
    "gabapentin", "neurontin", "pregabalin", "lyrica", "clonazepam", "klonopin",
    "prednisolone", "prednisone", "dexamethasone", "allopurinol", "colchicine"
]

def preprocess_image(image_path):
    """Enhance image for better OCR readability (contrast, sharpening, grayscale)."""
    try:
        with Image.open(image_path) as img:
            # Convert to grayscale
            gray = img.convert('L')
            # Increase contrast
            enhancer = ImageEnhance.Contrast(gray)
            enhanced = enhancer.enhance(1.8)
            # Apply slight sharpening
            sharpened = enhanced.filter(ImageFilter.SHARPEN)
            
            # Save preprocessed temp image
            preprocessed_path = image_path + "_preprocessed.png"
            sharpened.save(preprocessed_path)
            return preprocessed_path
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        return image_path

def perform_tesseract_ocr(image_path):
    """Attempts OCR using pytesseract if installed."""
    try:
        import pytesseract
        preprocessed = preprocess_image(image_path)
        text = pytesseract.image_to_string(Image.open(preprocessed))
        if os.path.exists(preprocessed) and preprocessed != image_path:
            os.remove(preprocessed)
        return text
    except Exception as e:
        logger.info(f"Tesseract OCR not active or failed: {e}")
        return ""

def perform_gemini_vision_ocr(image_path):
    """Attempts Gemini Vision API extraction if API key is provided."""
    if not Config.GEMINI_API_KEY:
        return ""
    try:
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        with Image.open(image_path) as img:
            prompt = (
                "Identify the exact medicine brand name, generic active ingredient, and strength (mg/mcg) "
                "visible on this medicine package or prescription label. "
                "Output just the detected medicine name and active ingredients."
            )
            response = model.generate_content([prompt, img])
            return response.text if response else ""
    except Exception as e:
        logger.warning(f"Gemini Vision call failed: {e}")
        return ""

def extract_medicine_name_from_text(raw_text, filename=""):
    """
    Extracts likely medicine name from OCR text or filename using regex and dictionary matching.
    """
    combined_corpus = f"{raw_text} {filename}".lower()
    
    # 1. Exact match in known medicines list
    for med in KNOWN_MEDS:
        pattern = r'\b' + re.escape(med) + r'\b'
        if re.search(pattern, combined_corpus):
            return med.title(), 0.95

    # 2. Dosage pattern extraction e.g. "Amoxicillin 500mg" or "Paracetamol 650 mg"
    dosage_match = re.search(r'([A-Za-z]{4,20})\s*(\d+\s*(?:mg|mcg|ml|g))', combined_corpus, re.IGNORECASE)
    if dosage_match:
        candidate = dosage_match.group(1).title()
        for med in KNOWN_MEDS:
            if med in candidate.lower() or candidate.lower() in med:
                return med.title(), 0.90
        return candidate, 0.70

    # 3. First prominent capitalized word in raw_text
    words = re.findall(r'[A-Za-z]{4,}', raw_text)
    for word in words:
        for med in KNOWN_MEDS:
            if med in word.lower() or word.lower() in med:
                return med.title(), 0.85

    # Fallback to first word or filename stem if nothing found
    if filename:
        clean_file = re.sub(r'[^a-zA-Z]', ' ', os.path.splitext(os.path.basename(filename))[0]).strip()
        for med in KNOWN_MEDS:
            if med in clean_file.lower():
                return med.title(), 0.80

    return "Unknown Medicine", 0.30

def process_medicine_image(image_path, original_filename=""):
    """
    Complete pipeline to analyze a medicine image file.
    Returns detected name, raw OCR text, confidence score, and processing method.
    """
    raw_text = ""
    method = "Regex / Smart Token Analysis"

    # Step 1: Try Gemini Vision if configured
    if Config.GEMINI_API_KEY:
        gemini_text = perform_gemini_vision_ocr(image_path)
        if gemini_text:
            raw_text = gemini_text
            method = "Google Gemini Vision AI"

    # Step 2: Fallback to Tesseract OCR
    if not raw_text:
        tesseract_text = perform_tesseract_ocr(image_path)
        if tesseract_text.strip():
            raw_text = tesseract_text
            method = "Tesseract OCR Engine"

    # Step 3: Extract medicine name
    detected_name, confidence = extract_medicine_name_from_text(raw_text, original_filename)

    return {
        "detected_name": detected_name,
        "raw_ocr_text": raw_text.strip() if raw_text else f"Visual extraction performed on {original_filename}",
        "confidence": confidence,
        "method": method
    }
