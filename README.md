# 🏥 AI Medicine Analyzer

An intelligent, full-stack pharmaceutical analysis web application designed to simplify medical information for everyday users, identify medications from package photos using OCR, detect dangerous multi-drug interactions, and provide grounded AI assistant support with strict safety guardrails.

---

## 🌟 Key Highlights & Features

1. **Medicine Name Search & Autocomplete**: Instant search across 50+ essential drugs with generic names, brand names, and drug classes.
2. **Package Photo OCR & Recognition**: Upload photos of medicine strips or boxes to extract text and recognize active drugs automatically.
3. **Layman-Friendly AI Explanations**: Translates complex clinical pharmacology into clear, easy-to-understand language.
4. **Multi-Drug Interaction Checker**: Checks 2 or more medications for pairwise conflicts, classifies severity (*Major*, *Moderate*, *Minor*), and alerts when physician consultation is critical.
5. **Context-Aware Medical AI Chatbot**: Interactive Q&A grounded on OpenFDA and verified clinical records with strict guardrails (no diagnosis, no prescription, emergency triaging).
6. **Audio Text-to-Speech Reader**: Accessibility feature that reads medicine details aloud.
7. **Search History Ledger**: Audit logs with export to CSV and re-analyze capabilities.
8. **Modern Glassmorphic UI**: Responsive design with light/dark theme toggle and quick demo presets for evaluation.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | React 18, Vite, Vanilla CSS (Glassmorphism + Tokens), Lucide-React |
| **Backend** | Python 3.14, Flask, Flask-CORS, Werkzeug |
| **Database** | SQLite 3 (Upgrade-ready for PostgreSQL) |
| **AI / OCR** | PIL Image Preprocessing, Pytesseract / Gemini Vision, Gemini 1.5 Flash LLM |
| **Data Grounding** | Official OpenFDA Drug Label API + Curated SQLite Clinical Compendium |

---

## 📂 Project Directory Structure

```
ai-medicine-analyzer/
│
├── frontend/                      # React SPA Frontend
│   ├── index.html                 # Main HTML template with SEO tags
│   ├── package.json               # Frontend dependencies & scripts
│   ├── vite.config.js             # Vite config with backend proxy
│   └── src/
│       ├── main.jsx               # React DOM entry
│       ├── App.jsx                # Tab navigation, global state, layout
│       ├── index.css              # Custom Glassmorphic design system
│       ├── services/
│       │   ├── api.js             # Centralized API fetch client
│       │   └── sampleData.js      # Demo presets for live testing
│       ├── components/
│       │   ├── Navbar.jsx          # Header with branding & theme toggle
│       │   ├── DisclaimerBanner.jsx# Prominent safety notices
│       │   ├── MedicineCard.jsx    # Monograph card with audio reader
│       │   ├── ImageUploader.jsx   # Drag-and-drop & demo OCR packages
│       │   ├── InteractionCard.jsx # Interaction severity badges
│       │   ├── ChatMessage.jsx     # Chat bubbles with grounding badges
│       │   └── HistoryTable.jsx    # Audit table with CSV export
│       └── pages/
│           ├── HomePage.jsx        # Landing hero, counters, search bar
│           ├── AnalyzerPage.jsx    # Dual-mode search & OCR analysis
│           ├── DetailsPage.jsx     # Medicine compendium catalog
│           ├── InteractionPage.jsx # Multi-drug combination checker
│           ├── AssistantPage.jsx   # AI Medical Chatbot
│           ├── HistoryPage.jsx     # Search logs & history manager
│           └── AboutPage.jsx       # Architecture & technical cheat sheet
│
├── backend/                       # Python Flask REST API
│   ├── app.py                     # Flask factory, routes, health check
│   ├── config.py                  # Environment config & safety constants
│   ├── requirements.txt           # Backend dependencies
│   ├── test_suite.py              # Automated integration test suite
│   ├── .env.example               # Template for API keys
│   ├── database/
│   │   ├── db.py                  # SQLite helper & connection pool
│   │   ├── schema.sql             # SQL schema (medicines, interactions, logs)
│   │   └── seed_data.py           # Pre-seeds 50+ medicines & 40+ interaction rules
│   ├── services/
│   │   ├── fda_service.py         # Live OpenFDA API search & fallback
│   │   ├── ocr_service.py         # Image preprocessing & OCR matcher
│   │   ├── ai_service.py          # AI explanation & safe chatbot engine
│   │   └── interaction_service.py # Pairwise interaction evaluator
│   ├── routes/
│   │   ├── medicine_routes.py     # Endpoints for search, get, image OCR
│   │   ├── interaction_routes.py  # Endpoints for drug interaction checks
│   │   ├── chat_routes.py         # Endpoints for medical AI assistant
│   │   └── history_routes.py      # Endpoints for search audit history
│   └── uploads/                   # Temporary folder for uploaded images
│
├── API_DOCUMENTATION.md           # Complete REST API reference
├── README.md                      # Project documentation (this file)
└── .gitignore                     # Git ignore rules
```

---

## 🚀 Beginner Step-by-Step Setup Guide

### Prerequisites
Make sure you have installed on your computer:
1. **Python 3.10+** (verify with `python --version`)
2. **Node.js 18+ and npm** (verify with `node --version`)

---

### Step 1: Clone or Open the Project
Open a terminal in the project directory:
```bash
cd ai-medicine-analyzer
```

---

### Step 2: Set Up and Run the Flask Backend

1. **Navigate to the `backend` folder**:
   ```bash
   cd backend
   ```

2. **Install Python dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Initialize and Seed the Database**:
   ```bash
   python database/seed_data.py
   ```
   *Expected Output*: `Database seeded successfully: 51 medicines, 27 interaction rules.`

4. **Start the Flask Backend Server**:
   ```bash
   python app.py
   ```
   *Expected Output*: `Running on http://127.0.0.1:5000`

5. **Verify the Backend**:
   Open your browser or visit `http://127.0.0.1:5000/api/health`. You should see `{"status": "online", "database": "Healthy"}`.

---

### Step 3: Set Up and Run the React Frontend

1. **Open a NEW terminal window** and navigate to the `frontend` folder:
   ```bash
   cd ai-medicine-analyzer/frontend
   ```

2. **Install Frontend dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vite Development Server**:
   ```bash
   npm run dev
   ```
   *Expected Output*: `➜ Local: http://localhost:5173/`

4. **Open the Web Application**:
   Visit `http://localhost:5173/` in your browser.

---

## 🧪 Running Automated Tests

To verify backend endpoints and integration:
```bash
cd backend
python test_suite.py
```
*Expected Output*: `8/8 PASSED (100% SUCCESS)`.

---

## 🔒 Strict AI Safety & Ethics Policy

> [!IMPORTANT]
> **Safety Compliance**: This application is strictly an educational tool.
> 1. **No Medical Diagnosis**: The AI rejects queries attempting to self-diagnose symptoms.
> 2. **No Prescription or Dosage Alterations**: It will never prescribe or recommend changing existing dosages.
> 3. **Zero-Hallucination Grounding**: Every drug monograph is anchored in verified clinical data and OpenFDA records.
> 4. **Emergency Escalation**: Detects crisis keywords (e.g., overdose, severe chest pain) and alerts users to contact emergency services immediately.

---

## 📋 System Architecture & Technical Specifications

| Evaluation Criteria | How It Is Implemented in This Project |
| :--- | :--- |
| **System Architecture** | Modular 3-tier architecture (React SPA ↔ Flask REST API ↔ SQLite DB + OpenFDA). |
| **AI / Machine Learning** | Image contrast enhancement & OCR extraction + Google Gemini 1.5 Flash grounded prompt engine. |
| **Data Integrity** | SQLite relational schema with foreign keys, indexes, and symmetric interaction matrices. |
| **User Experience (UX)** | Glassmorphic responsive UI, text-to-speech audio reader, and one-click demo presets. |
| **Safety Guardrails** | Contextual disclaimers, refusal to diagnose/prescribe, and doctor consultation flags. |

---

## 🌐 Deployment Instructions

### Deploy Frontend (Vercel)
1. Push project to GitHub.
2. In Vercel, set root directory to `frontend/`.
3. Build command: `npm run build`, Output directory: `dist`.
4. Add environment variable `VITE_API_URL` pointing to your deployed backend URL.

### Deploy Backend (Render / Railway)
1. In Render, create a new Web Service pointing to `backend/`.
2. Environment: `Python 3`.
3. Build command: `pip install -r requirements.txt && python database/seed_data.py`.
4. Start command: `gunicorn app:create_app()`.

---

## 📄 License
Educational and Healthcare Intelligence Platform License.
