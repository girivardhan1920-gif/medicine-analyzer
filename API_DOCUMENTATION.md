# AI Medicine Analyzer - REST API Specification

This document details all backend endpoints provided by the Flask REST API server (`http://127.0.0.1:5000`).

---

## 1. System & Health Endpoints

### `GET /api/health`
Checks server status, database health, and total medicine/interaction rules loaded.

**Sample Response:**
```json
{
  "database": "Healthy",
  "gemini_ai_configured": false,
  "safety_disclaimer": "EDUCATIONAL USE ONLY: This information is for educational purposes...",
  "service": "AI Medicine Analyzer API",
  "status": "online",
  "total_interaction_rules": 54,
  "total_medicines_indexed": 51,
  "version": "1.0.0"
}
```

### `GET /api/stats`
Returns aggregated metrics for the dashboard view.

**Sample Response:**
```json
{
  "success": true,
  "stats": {
    "total_medicines": 51,
    "known_interactions": 54,
    "total_queries_processed": 18,
    "therapeutic_categories": 9
  }
}
```

---

## 2. Medicine Information & Analysis Endpoints

### `GET /api/medicine/search?q=<query>`
Performs fuzzy and prefix search across brand names, generic active ingredients, and therapeutic categories.

**Query Parameters:**
- `q` (string): Search query (e.g. `paracetamol`, `amox`)

**Sample Response:**
```json
{
  "count": 1,
  "query": "paracetamol",
  "results": [
    {
      "brand_names": "Tylenol, Panadol, Calpol, Crocin, Dolo 650",
      "category": "Analgesic & Antipyretic",
      "common_uses": "Relief of mild to moderate pain...",
      "generic_name": "Acetaminophen",
      "id": 1,
      "name": "Paracetamol"
    }
  ],
  "success": true
}
```

### `GET /api/medicine/<medicine_name>`
Retrieves full pharmacological monograph with AI explanation and OpenFDA fallback.

**Path Parameters:**
- `medicine_name` (string): Exact or partial name (e.g. `Amoxicillin`, `Lipitor`)

**Sample Response:**
```json
{
  "success": true,
  "source": "Local Verified Database",
  "data": {
    "name": "Amoxicillin",
    "generic_name": "Amoxicillin Trihydrate",
    "brand_names": "Amoxil, Moxatag, Augmentin",
    "category": "Antibiotic (Penicillin class)",
    "common_uses": "Treatment of bacterial infections including ear infections...",
    "general_precautions": "Complete the entire prescribed course even if symptoms improve...",
    "common_side_effects": "Diarrhea, mild nausea, vomiting, skin rash...",
    "warnings": "Contraindicated in individuals with severe penicillin allergy...",
    "storage_info": "Capsules: 20°C-25°C dry place...",
    "dosage_forms": "Capsule, Tablet, Oral Suspension",
    "prescription_required": 1
  },
  "ai_explanation": {
    "summary": "Amoxicillin (Amoxicillin Trihydrate) belongs to the class of antibiotic (penicillin class)...",
    "key_takeaways": [
      "Primary Purpose: Bacterial infections",
      "Key Safety Caution: Complete course",
      "Storage: Room temperature or refrigerator"
    ],
    "grounded_on": "Verified Pharmaceutical Database & OpenFDA Records"
  },
  "disclaimer": "EDUCATIONAL USE ONLY: ..."
}
```

### `POST /api/medicine/analyze`
Submits a drug name for deep analysis, generates layman summaries, and logs the query to history.

**Request Body (`application/json`):**
```json
{
  "medicine_name": "Metformin"
}
```

### `POST /api/medicine/image`
Uploads a medicine package photo, executes OCR preprocessing and text recognition, identifies active drugs, and returns complete analysis.

**Request (`multipart/form-data`):**
- `image`: Image binary file (PNG, JPG, WEBP)

**Sample Response:**
```json
{
  "success": true,
  "matched": true,
  "ocr_details": {
    "confidence": 0.95,
    "detected_name": "Amoxicillin",
    "method": "Regex / Smart Token Analysis",
    "raw_ocr_text": "AMOXICILLIN 500mg CAPSULES"
  },
  "medicine": { ... },
  "ai_analysis": { ... },
  "disclaimer": "EDUCATIONAL USE ONLY: ..."
}
```

---

## 3. Multi-Drug Interaction Endpoints

### `POST /api/interactions/check`
Checks 2 or more medications for pairwise clinical drug-drug interactions and returns severity classifications.

**Request Body (`application/json`):**
```json
{
  "medicines": ["Aspirin", "Warfarin"]
}
```

**Sample Response:**
```json
{
  "success": true,
  "data": {
    "drugs_checked": ["Aspirin", "Warfarin"],
    "total_interactions": 2,
    "major_count": 2,
    "moderate_count": 0,
    "minor_count": 0,
    "risk_level": "HIGH RISK (Major Interactions Detected)",
    "consultation_recommended": true,
    "consultation_message": "⚠️ Potential interaction identified. We strongly advise consulting your doctor or pharmacist before combining these medications.",
    "interactions": [
      {
        "drug_a": "Aspirin",
        "drug_b": "Warfarin",
        "severity": "Major",
        "description": "Concurrent use of Aspirin with Warfarin produces a synergistic effect that dramatically amplifies the risk of major gastrointestinal and systemic bleeding.",
        "recommendation": "Avoid combination unless specifically directed and monitored by a cardiologist/hematologist."
      }
    ]
  },
  "disclaimer": "EDUCATIONAL USE ONLY: ..."
}
```

### `GET /api/interactions/common`
Returns pre-configured clinical trial pairs for quick testing in demos.

---

## 4. AI Assistant Endpoints

### `POST /api/chat`
Context-aware medical Q&A with strict safety guardrails.

**Request Body (`application/json`):**
```json
{
  "message": "What are the common side effects of Lisinopril?",
  "session_id": "demo-session"
}
```

**Sample Response:**
```json
{
  "success": true,
  "matched_drug": "Lisinopril",
  "reply": "**Common Side Effects of Lisinopril (Lisinopril)**:\nPersistent dry cough, dizziness, headache, excessive fatigue.\n\n⚠️ Disclaimer: This AI analysis is for informational & educational purposes only...",
  "safety_flag": 0,
  "disclaimer": "EDUCATIONAL USE ONLY: ..."
}
```

---

## 5. History & Audit Endpoints

### `GET /api/history?type=<type>&limit=50`
Retrieves search logs with optional type filter (`text`, `image_ocr`, `interaction`).

### `DELETE /api/history/<id>`
Deletes a specific log entry.

### `POST /api/history/clear`
Wipes the entire search history ledger.
