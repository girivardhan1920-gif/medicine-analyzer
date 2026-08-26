-- AI Medicine Analyzer Database Schema

CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    generic_name TEXT NOT NULL,
    brand_names TEXT,
    manufacturer TEXT,
    category TEXT NOT NULL,
    common_uses TEXT NOT NULL,
    general_precautions TEXT NOT NULL,
    common_side_effects TEXT NOT NULL,
    warnings TEXT NOT NULL,
    storage_info TEXT NOT NULL,
    dosage_forms TEXT DEFAULT 'Tablet, Capsule',
    prescription_required INTEGER DEFAULT 0,
    fda_ndc TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS drug_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_a TEXT NOT NULL,
    drug_b TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('Major', 'Moderate', 'Minor')),
    description TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(drug_a, drug_b)
);

CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    search_type TEXT NOT NULL, -- 'text', 'image_ocr', 'interaction'
    result_summary TEXT,
    matched_medicine TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    safety_flag INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices for rapid search and autocomplete
CREATE INDEX IF NOT EXISTS idx_medicines_name ON medicines(name COLLATE NOCASE);
CREATE INDEX IF NOT EXISTS idx_medicines_generic ON medicines(generic_name COLLATE NOCASE);
CREATE INDEX IF NOT EXISTS idx_medicines_category ON medicines(category);
CREATE INDEX IF NOT EXISTS idx_interactions_drugs ON drug_interactions(drug_a COLLATE NOCASE, drug_b COLLATE NOCASE);
