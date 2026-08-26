"""
Seed Data for AI Medicine Analyzer.
Populates SQLite with 50+ common medicines and 40+ multi-drug interaction matrices.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.db import get_db_connection, init_db

MEDICINES_DATA = [
    # 1. Analgesics / Antipyretics / NSAIDs
    {
        "name": "Paracetamol",
        "generic_name": "Acetaminophen",
        "brand_names": "Tylenol, Panadol, Calpol, Crocin, Dolo 650",
        "manufacturer": "GSK / Johnson & Johnson / Micro Labs",
        "category": "Analgesic & Antipyretic",
        "common_uses": "Relief of mild to moderate pain (headache, toothache, backache, arthritis) and fever reduction.",
        "general_precautions": "Do not exceed maximum daily dose (4,000 mg/day for adults). Avoid heavy alcohol consumption. Check for acetaminophen in other combination cold/flu remedies to prevent accidental overdose.",
        "common_side_effects": "Generally well-tolerated. Rare: mild nausea, allergic skin rash, itching.",
        "warnings": "Acute overdose can cause severe, life-threatening liver damage (hepatic necrosis). Seek emergency care immediately if overdose is suspected.",
        "storage_info": "Store at room temperature (15°C to 25°C), away from moisture and direct sunlight. Keep out of reach of children.",
        "dosage_forms": "Tablet (500mg, 650mg), Syrup, Effervescent tablet, IV Infusion",
        "prescription_required": 0,
        "fda_ndc": "50580-488"
    },
    {
        "name": "Ibuprofen",
        "generic_name": "Ibuprofen",
        "brand_names": "Advil, Motrin, Brufen, Nurofen",
        "manufacturer": "Pfizer / Reckitt / Abbott",
        "category": "NSAID (Non-Steroidal Anti-Inflammatory)",
        "common_uses": "Relief of pain, inflammation, swelling, dental pain, menstrual cramps, migraine, and osteoarthritis.",
        "general_precautions": "Take with food or milk to reduce stomach upset. Caution in individuals with history of stomach ulcers, kidney disease, or cardiovascular disorders.",
        "common_side_effects": "Stomach pain, heartburn, indigestion, dizziness, mild nausea.",
        "warnings": "Increases risk of serious gastrointestinal bleeding, ulceration, and cardiovascular thrombotic events (heart attack, stroke) with chronic high-dose use.",
        "storage_info": "Store below 25°C in a tightly closed container. Protect from excess heat and moisture.",
        "dosage_forms": "Tablet (200mg, 400mg, 600mg), Capsule, Oral Suspension, Topical Gel",
        "prescription_required": 0,
        "fda_ndc": "0573-0164"
    },
    {
        "name": "Aspirin",
        "generic_name": "Acetylsalicylic Acid",
        "brand_names": "Bayer Aspirin, Ecosprin, Disprin",
        "manufacturer": "Bayer / USV Ltd",
        "category": "NSAID & Antiplatelet Agent",
        "common_uses": "Secondary prevention of cardiovascular events (heart attack, ischemic stroke), pain relief, and inflammation reduction.",
        "general_precautions": "Take with meals. Avoid in children and teenagers recovering from viral infections due to risk of Reye's syndrome.",
        "common_side_effects": "Gastric irritation, heartburn, easy bruising, minor bleeding.",
        "warnings": "Risk of serious gastrointestinal hemorrhage. Contraindicated in patients with active bleeding ulcers or severe bleeding disorders.",
        "storage_info": "Store at 20°C to 25°C in a dry environment. Keep bottle tightly closed.",
        "dosage_forms": "Enteric-coated tablet (75mg, 81mg, 325mg, 500mg)",
        "prescription_required": 0,
        "fda_ndc": "0280-2100"
    },
    {
        "name": "Naproxen",
        "generic_name": "Naproxen Sodium",
        "brand_names": "Aleve, Naprosyn, Anaprox",
        "manufacturer": "Bayer / Roche",
        "category": "NSAID",
        "common_uses": "Relief of joint pain, ankylosing spondylitis, tendonitis, bursitis, acute gout, and menstrual cramps.",
        "general_precautions": "Take with a full glass of water and food. Do not lie down for 10 minutes after swallowing.",
        "common_side_effects": "Drowsiness, headache, dizziness, constipation, mild heartburn.",
        "warnings": "May increase risk of heart attack or stroke; can cause gastrointestinal ulcers and kidney impairment.",
        "storage_info": "Store at 15°C to 30°C. Protect from light.",
        "dosage_forms": "Tablet (220mg, 250mg, 500mg), Extended-release",
        "prescription_required": 0,
        "fda_ndc": "0280-6000"
    },
    {
        "name": "Tramadol",
        "generic_name": "Tramadol Hydrochloride",
        "brand_names": "Ultram, Tramal, Ultracet",
        "manufacturer": "Janssen / Grunenthal",
        "category": "Opioid Analgesic",
        "common_uses": "Management of moderate to moderately severe acute and chronic pain.",
        "general_precautions": "High potential for dependence and tolerance. Do not combine with alcohol or sedatives. Avoid driving or operating machinery.",
        "common_side_effects": "Dizziness, somnolence, nausea, constipation, dry mouth, sweating.",
        "warnings": "Risk of respiratory depression, addiction, and Serotonin Syndrome when combined with serotonergic drugs (SSRIs/SNRIs).",
        "storage_info": "Store in a secure, locked cabinet at room temperature (20°C to 25°C).",
        "dosage_forms": "Tablet (50mg, 100mg), Extended-release, Injection",
        "prescription_required": 1,
        "fda_ndc": "50458-650"
    },

    # 2. Antibiotics & Antimicrobials
    {
        "name": "Amoxicillin",
        "generic_name": "Amoxicillin Trihydrate",
        "brand_names": "Amoxil, Moxatag, Augmentin (with Clavulanate)",
        "manufacturer": "GSK / Sandoz / Teva",
        "category": "Antibiotic (Penicillin class)",
        "common_uses": "Treatment of bacterial infections including ear infections (otitis media), strep throat, pneumonia, skin infections, and urinary tract infections.",
        "general_precautions": "Complete the entire prescribed course even if symptoms improve. Ineffective against viral infections like the common cold or flu.",
        "common_side_effects": "Diarrhea, mild nausea, vomiting, skin rash, oral thrush.",
        "warnings": "Contraindicated in individuals with severe penicillin allergy (anaphylaxis risk). Discontinue and seek urgent care if severe watery diarrhea occurs.",
        "storage_info": "Capsules: 20°C-25°C dry place. Liquid suspension: Store in refrigerator (2°C-8°C) and discard after 14 days.",
        "dosage_forms": "Capsule (250mg, 500mg), Tablet (875mg), Oral Suspension (125mg/5mL, 250mg/5mL)",
        "prescription_required": 1,
        "fda_ndc": "0781-2613"
    },
    {
        "name": "Azithromycin",
        "generic_name": "Azithromycin",
        "brand_names": "Zithromax, Z-Pak, Azithral",
        "manufacturer": "Pfizer / Lupin / Cipla",
        "category": "Antibiotic (Macrolide)",
        "common_uses": "Respiratory tract infections, bronchitis, community-acquired pneumonia, sinusitis, skin infections, and certain sexually transmitted infections.",
        "general_precautions": "Can be taken with or without food. Avoid taking aluminum or magnesium antacids simultaneously as they reduce absorption.",
        "common_side_effects": "Diarrhea, abdominal cramps, nausea, transient headache.",
        "warnings": "Can cause QT interval prolongation and cardiac arrhythmias, especially in patients with preexisting heart conditions or electrolyte imbalances.",
        "storage_info": "Store at 15°C to 30°C in a tightly sealed container.",
        "dosage_forms": "Tablet (250mg, 500mg), Oral Suspension, IV Infusion",
        "prescription_required": 1,
        "fda_ndc": "0069-3060"
    },
    {
        "name": "Ciprofloxacin",
        "generic_name": "Ciprofloxacin Hydrochloride",
        "brand_names": "Cipro, Ciplox, Ciproxin",
        "manufacturer": "Bayer / Cipla",
        "category": "Antibiotic (Fluoroquinolone)",
        "common_uses": "Complicated urinary tract infections, severe bacterial diarrhea, bone and joint infections, and intra-abdominal infections.",
        "general_precautions": "Drink plenty of fluids to avoid crystalluria. Avoid excessive sunlight/UV exposure due to photosensitivity. Do not take with dairy or mineral supplements.",
        "common_side_effects": "Nausea, diarrhea, dizziness, lightheadedness, insomnia.",
        "warnings": "Black Box Warning: Increased risk of tendinitis and tendon rupture (especially Achilles tendon), peripheral neuropathy, and CNS toxicities.",
        "storage_info": "Store at 20°C to 25°C. Keep dry and protected from light.",
        "dosage_forms": "Tablet (250mg, 500mg, 750mg), Eye drops, IV Infusion",
        "prescription_required": 1,
        "fda_ndc": "50419-402"
    },
    {
        "name": "Doxycycline",
        "generic_name": "Doxycycline Hyclate",
        "brand_names": "Vibramycin, Doryx, Monodox",
        "manufacturer": "Pfizer / Mayne Pharma",
        "category": "Antibiotic (Tetracycline)",
        "common_uses": "Acne vulgaris, Lyme disease, respiratory infections, chlamydia, and malaria prophylaxis.",
        "general_precautions": "Take with a full glass of water and remain upright for at least 30 minutes to prevent esophageal ulceration. Avoid strong sun exposure.",
        "common_side_effects": "Nausea, photosensitivity (sunburn), esophageal irritation, diarrhea.",
        "warnings": "Avoid during pregnancy, breastfeeding, and in children under 8 years due to permanent tooth discoloration and enamel hypoplasia.",
        "storage_info": "Store at 15°C to 30°C. Protect from light.",
        "dosage_forms": "Capsule (50mg, 100mg), Tablet",
        "prescription_required": 1,
        "fda_ndc": "0069-0940"
    },
    {
        "name": "Cephalexin",
        "generic_name": "Cephalexin",
        "brand_names": "Keflex, Sporidex",
        "manufacturer": "Prasco / Sun Pharma",
        "category": "Antibiotic (First-Gen Cephalosporin)",
        "common_uses": "Skin and soft tissue infections, strep pharyngitis, bone infections, UTI.",
        "general_precautions": "Use caution if patient has a history of mild penicillin allergy (1-10% cross-reactivity).",
        "common_side_effects": "Diarrhea, nausea, indigestion, abdominal pain.",
        "warnings": "Pseudomembranous colitis associated with Clostridioides difficile overgrowth.",
        "storage_info": "Store capsules at room temperature; reconstituted suspension in refrigerator for up to 14 days.",
        "dosage_forms": "Capsule (250mg, 500mg), Oral Suspension",
        "prescription_required": 1,
        "fda_ndc": "66993-410"
    },

    # 3. Cardiovascular & Antihypertensive
    {
        "name": "Amlodipine",
        "generic_name": "Amlodipine Besylate",
        "brand_names": "Norvasc, Amlong, Stamlo",
        "manufacturer": "Pfizer / Dr. Reddy's",
        "category": "Antihypertensive (Calcium Channel Blocker)",
        "common_uses": "Management of high blood pressure (hypertension) and coronary artery disease / angina pectoris.",
        "general_precautions": "Take consistently at the same time each day. Avoid sudden standing to prevent orthostatic dizziness.",
        "common_side_effects": "Peripheral edema (swelling of ankles/feet), flushing, dizziness, fatigue, palpitations.",
        "warnings": "May exacerbate severe aortic stenosis or worsen angina upon initial dosing in rare instances.",
        "storage_info": "Store at 15°C to 30°C. Protect from moisture.",
        "dosage_forms": "Tablet (2.5mg, 5mg, 10mg)",
        "prescription_required": 1,
        "fda_ndc": "0069-1530"
    },
    {
        "name": "Lisinopril",
        "generic_name": "Lisinopril",
        "brand_names": "Prinivil, Zestril, Listril",
        "manufacturer": "AstraZeneca / Merck",
        "category": "Antihypertensive (ACE Inhibitor)",
        "common_uses": "Treatment of hypertension, heart failure, and improving post-myocardial infarction survival.",
        "general_precautions": "Avoid potassium supplements or high-potassium salt substitutes unless prescribed. Monitor kidney function and serum electrolytes.",
        "common_side_effects": "Persistent dry cough, dizziness, headache, excessive fatigue.",
        "warnings": "Black Box Warning: Fetal toxicity (contraindicated in pregnancy). Risk of life-threatening angioedema (swelling of face, lips, tongue, or airway).",
        "storage_info": "Store at 20°C to 25°C. Protect from moisture and excessive heat.",
        "dosage_forms": "Tablet (2.5mg, 5mg, 10mg, 20mg, 40mg)",
        "prescription_required": 1,
        "fda_ndc": "0310-0130"
    },
    {
        "name": "Losartan",
        "generic_name": "Losartan Potassium",
        "brand_names": "Cozaar, Losar, Repace",
        "manufacturer": "Organon / Sun Pharma",
        "category": "Antihypertensive (ARB - Angiotensin Receptor Blocker)",
        "common_uses": "Hypertension, diabetic nephropathy in type 2 diabetes, stroke risk reduction in left ventricular hypertrophy.",
        "general_precautions": "Stay adequately hydrated. Inform your doctor if you experience muscle weakness or irregular heartbeat.",
        "common_side_effects": "Dizziness, nasal congestion, back pain, fatigue.",
        "warnings": "Black Box Warning: Fetal injury and death if taken during pregnancy. Discontinue as soon as pregnancy is detected.",
        "storage_info": "Store at 20°C to 25°C in a dry location.",
        "dosage_forms": "Tablet (25mg, 50mg, 100mg)",
        "prescription_required": 1,
        "fda_ndc": "0006-0951"
    },
    {
        "name": "Metoprolol",
        "generic_name": "Metoprolol Succinate / Tartrate",
        "brand_names": "Toprol-XL, Lopressor, Betaloc",
        "manufacturer": "AstraZeneca / Novartis",
        "category": "Beta-Blocker (Cardioselective)",
        "common_uses": "Hypertension, angina, stable heart failure, post-myocardial infarction cardioprotection, arrhythmia.",
        "general_precautions": "Do not stop taking abruptly as it can cause rebound hypertension or severe cardiac events. Take with or immediately following a meal.",
        "common_side_effects": "Bradycardia (slow heart rate), tiredness, dizziness, cold extremities, sleep disturbances.",
        "warnings": "Abrupt cessation can precipitate angina or myocardial infarction. Caution in severe asthma and severe bradycardia.",
        "storage_info": "Store at 15°C to 30°C.",
        "dosage_forms": "Tablet (Tartrate 25/50/100mg, Succinate ER 25/50/100/200mg)",
        "prescription_required": 1,
        "fda_ndc": "0186-1090"
    },
    {
        "name": "Atorvastatin",
        "generic_name": "Atorvastatin Calcium",
        "brand_names": "Lipitor, Atorva, Storvas",
        "manufacturer": "Pfizer / Zydus",
        "category": "HMG-CoA Reductase Inhibitor (Statin)",
        "common_uses": "Hypercholesterolemia, dyslipidemia, and prevention of cardiovascular events (heart attack, stroke).",
        "general_precautions": "Avoid consuming large quantities of grapefruit juice. Follow a heart-healthy cholesterol-lowering diet.",
        "common_side_effects": "Mild joint pain, diarrhea, indigestion, nasopharyngitis.",
        "warnings": "Risk of myopathy and rare rhabdomyolysis (severe muscle breakdown). Promptly report unexplained muscle pain, tenderness, or dark brown urine.",
        "storage_info": "Store at 20°C to 25°C. Keep away from moisture.",
        "dosage_forms": "Tablet (10mg, 20mg, 40mg, 80mg)",
        "prescription_required": 1,
        "fda_ndc": "0071-0155"
    },
    {
        "name": "Rosuvastatin",
        "generic_name": "Rosuvastatin Calcium",
        "brand_names": "Crestor, Rosuvas, Rozavel",
        "manufacturer": "AstraZeneca / Sun Pharma",
        "category": "HMG-CoA Reductase Inhibitor (Statin)",
        "common_uses": "Management of primary hyperlipidemia, mixed dyslipidemia, and slowing progression of atherosclerosis.",
        "general_precautions": "Periodic liver enzyme monitoring recommended. Avoid antacids within 2 hours of dose.",
        "common_side_effects": "Headache, muscle ache, abdominal pain, asthenia (weakness).",
        "warnings": "Rare risk of immune-mediated necrotizing myopathy and hepatic transaminase elevation.",
        "storage_info": "Store at 20°C to 25°C.",
        "dosage_forms": "Tablet (5mg, 10mg, 20mg, 40mg)",
        "prescription_required": 1,
        "fda_ndc": "0310-0755"
    },
    {
        "name": "Hydrochlorothiazide",
        "generic_name": "Hydrochlorothiazide (HCTZ)",
        "brand_names": "Microzide, Esidrix, Aquazide",
        "manufacturer": "Actavis / Watson",
        "category": "Thiazide Diuretic",
        "common_uses": "Hypertension management and edema associated with heart failure, cirrhosis, or kidney disease.",
        "general_precautions": "Take in the morning to avoid nighttime urination (nocturia). Monitor electrolytes (potassium, sodium).",
        "common_side_effects": "Frequent urination, mild dehydration, electrolyte imbalance, hypokalemia, dizziness.",
        "warnings": "Can exacerbate hyperuricemia/gout and cause acute myopia or secondary angle-closure glaucoma.",
        "storage_info": "Store at 20°C to 25°C in a tightly closed container.",
        "dosage_forms": "Tablet (12.5mg, 25mg, 50mg), Capsule",
        "prescription_required": 1,
        "fda_ndc": "0093-0138"
    },
    {
        "name": "Furosemide",
        "generic_name": "Furosemide",
        "brand_names": "Lasix, Frusid",
        "manufacturer": "Sanofi / Torrent",
        "category": "Loop Diuretic",
        "common_uses": "Edema linked to congestive heart failure, liver cirrhosis, nephrotic syndrome, and acute pulmonary edema.",
        "general_precautions": "Monitor blood pressure, kidney function, and serum potassium regularly. Maintain adequate fluid balance.",
        "common_side_effects": "Excessive urination, dizziness, dehydration, cramping, electrolyte depletion.",
        "warnings": "Black Box Warning: Potent diuretic that in excessive amounts leads to profound water and electrolyte depletion.",
        "storage_info": "Store at 15°C to 30°C. Protect from light.",
        "dosage_forms": "Tablet (20mg, 40mg, 80mg), Oral Solution, Injection",
        "prescription_required": 1,
        "fda_ndc": "0039-0060"
    },
    {
        "name": "Warfarin",
        "generic_name": "Warfarin Sodium",
        "brand_names": "Coumadin, Jantoven, Marevan",
        "manufacturer": "Bristol Myers Squibb",
        "category": "Anticoagulant (Vitamin K Antagonist)",
        "common_uses": "Prophylaxis and treatment of deep vein thrombosis (DVT), pulmonary embolism (PE), atrial fibrillation thromboembolism, and mechanical heart valve clotting.",
        "general_precautions": "Requires strict, regular INR (blood clotting time) blood tests. Maintain a consistent dietary intake of Vitamin K (green leafy vegetables).",
        "common_side_effects": "Bleeding gums, easy bruising, nosebleeds, extended bleeding from cuts.",
        "warnings": "Black Box Warning: Can cause major or fatal hemorrhage. Do not take NSAIDs, Aspirin, or herbal supplements without medical approval.",
        "storage_info": "Store at 20°C to 25°C. Protect from light and moisture.",
        "dosage_forms": "Tablet (1mg, 2mg, 2.5mg, 5mg, 7.5mg, 10mg)",
        "prescription_required": 1,
        "fda_ndc": "0590-0010"
    },
    {
        "name": "Clopidogrel",
        "generic_name": "Clopidogrel Bisulfate",
        "brand_names": "Plavix, Clopilet, Deplatt",
        "manufacturer": "Sanofi / Sun Pharma",
        "category": "Antiplatelet Agent (P2Y12 Inhibitor)",
        "common_uses": "Prevention of atherothrombotic events in patients with recent myocardial infarction, stroke, or established peripheral arterial disease / stents.",
        "general_precautions": "Take once daily with or without food. Inform dentists and surgeons of use prior to scheduled procedures.",
        "common_side_effects": "Bruising, epistaxis (nosebleeds), minor gastrointestinal discomfort.",
        "warnings": "Black Box Warning: Diminished effectiveness in poor CYP2C19 metabolizers. Elevated bleeding risk when combined with anticoagulants.",
        "storage_info": "Store at 25°C.",
        "dosage_forms": "Tablet (75mg, 300mg)",
        "prescription_required": 1,
        "fda_ndc": "0024-5850"
    },

    # 4. Endocrine & Diabetes
    {
        "name": "Metformin",
        "generic_name": "Metformin Hydrochloride",
        "brand_names": "Glucophage, Glycomet, Fortamet",
        "manufacturer": "Merck / USV Ltd",
        "category": "Antidiabetic (Biguanide)",
        "common_uses": "First-line pharmacological management of Type 2 Diabetes Mellitus and polycystic ovary syndrome (PCOS).",
        "general_precautions": "Take with meals to minimize gastrointestinal disturbances. Discontinue temporarily prior to iodinated radiocontrast imaging procedures.",
        "common_side_effects": "Diarrhea, nausea, flatulence, abdominal bloating, metallic taste, vitamin B12 deficiency with long-term use.",
        "warnings": "Black Box Warning: Lactic acidosis (rare but severe medical emergency), especially in patients with acute renal impairment or sepsis.",
        "storage_info": "Store at 20°C to 25°C in a light-resistant container.",
        "dosage_forms": "Tablet (500mg, 850mg, 1000mg), Extended-Release (XR 500mg, 750mg, 1000mg)",
        "prescription_required": 1,
        "fda_ndc": "0087-6060"
    },
    {
        "name": "Glimepiride",
        "generic_name": "Glimepiride",
        "brand_names": "Amaryl, Glimy, Zoryl",
        "manufacturer": "Sanofi / Intas",
        "category": "Antidiabetic (Sulfonylurea)",
        "common_uses": "Glycemic control in adults with type 2 diabetes mellitus.",
        "general_precautions": "Take with breakfast or the first main meal of the day. Carry fast-acting glucose (candy or glucose tablets) in case of low blood sugar.",
        "common_side_effects": "Hypoglycemia (sweating, tremors, confusion), weight gain, nausea.",
        "warnings": "High risk of profound hypoglycemia if meals are skipped or delayed or during prolonged strenuous exercise.",
        "storage_info": "Store below 25°C.",
        "dosage_forms": "Tablet (1mg, 2mg, 3mg, 4mg)",
        "prescription_required": 1,
        "fda_ndc": "0039-0221"
    },
    {
        "name": "Sitagliptin",
        "generic_name": "Sitagliptin Phosphate",
        "brand_names": "Januvia, Istavel",
        "manufacturer": "Merck & Co. / Sun Pharma",
        "category": "Antidiabetic (DPP-4 Inhibitor)",
        "common_uses": "Monotherapy or combination therapy for glycemic control in Type 2 Diabetes.",
        "general_precautions": "Can be taken with or without food. Dose adjustment required in moderate to severe renal impairment.",
        "common_side_effects": "Upper respiratory tract infection, nasopharyngitis, headache.",
        "warnings": "Postmarketing reports of acute pancreatitis. Severe and disabling joint pain reported rarely.",
        "storage_info": "Store at 20°C to 25°C.",
        "dosage_forms": "Tablet (25mg, 50mg, 100mg)",
        "prescription_required": 1,
        "fda_ndc": "0006-0577"
    },
    {
        "name": "Levothyroxine",
        "generic_name": "Levothyroxine Sodium (T4)",
        "brand_names": "Synthroid, Levoxyl, Eltroxin, Thyronorm",
        "manufacturer": "AbbVie / Abbott",
        "category": "Thyroid Hormone Replacement",
        "common_uses": "Treatment of hypothyroidism (underactive thyroid) and pituitary TSH suppression in thyroid nodules/cancer.",
        "general_precautions": "Must be taken on an empty stomach with water, 30 to 60 minutes before breakfast. Separate from calcium, iron, or antacid supplements by at least 4 hours.",
        "common_side_effects": "Usually symptom-free when dosed accurately. Overdose causes signs of hyperthyroidism: heart palpitations, tremor, weight loss, heat intolerance, anxiety.",
        "warnings": "Black Box Warning: Not to be used for the treatment of obesity or weight loss. In euthyroid patients, weight reduction doses produce serious life-threatening toxicities.",
        "storage_info": "Store at 15°C to 30°C in a dry location away from direct light and moisture.",
        "dosage_forms": "Tablet (25mcg, 50mcg, 75mcg, 88mcg, 100mcg, 112mcg, 125mcg, 150mcg)",
        "prescription_required": 1,
        "fda_ndc": "0074-6594"
    },

    # 5. Gastrointestinal (PPIs, H2 Blockers, Antiemetics)
    {
        "name": "Omeprazole",
        "generic_name": "Omeprazole",
        "brand_names": "Prilosec, Omez, Losec",
        "manufacturer": "AstraZeneca / Dr. Reddy's",
        "category": "Proton Pump Inhibitor (PPI)",
        "common_uses": "Gastroesophageal reflux disease (GERD), acid reflux, peptic ulcer disease, heartburn, and Zollinger-Ellison syndrome.",
        "general_precautions": "Take 30-60 minutes before a meal (preferably breakfast). Swallow whole; do not crush or chew delayed-release capsules/tablets.",
        "common_side_effects": "Headache, abdominal pain, nausea, diarrhea, flatulence.",
        "warnings": "Long-term usage (>1 year) is associated with increased risk of bone fractures (osteoporosis), hypomagnesemia, vitamin B12 deficiency, and C. difficile-associated diarrhea.",
        "storage_info": "Store at room temperature (15°C to 30°C) protected from humidity and light.",
        "dosage_forms": "Delayed-release capsule (10mg, 20mg, 40mg), Powder for suspension",
        "prescription_required": 0,
        "fda_ndc": "0186-0742"
    },
    {
        "name": "Pantoprazole",
        "generic_name": "Pantoprazole Sodium",
        "brand_names": "Protonix, Pantocid, Pan 40",
        "manufacturer": "Pfizer / Alkem",
        "category": "Proton Pump Inhibitor (PPI)",
        "common_uses": "Erosive esophagitis associated with GERD, pathological hypersecretion, and gastric ulcer healing.",
        "general_precautions": "Best taken in the morning before breakfast with a glass of water.",
        "common_side_effects": "Headache, dizziness, joint pain, mild diarrhea.",
        "warnings": "Long-term use may reduce magnesium absorption and impair calcium assimilation.",
        "storage_info": "Store at 20°C to 25°C.",
        "dosage_forms": "Delayed-release tablet (20mg, 40mg), IV Injection",
        "prescription_required": 0,
        "fda_ndc": "0008-0841"
    },
    {
        "name": "Ranitidine",
        "generic_name": "Famotidine / Ranitidine (Famotidine preferred)",
        "brand_names": "Pepcid, Rantac, Zantac 360",
        "manufacturer": "Johnson & Johnson / JB Chemicals",
        "category": "H2 Receptor Antagonist",
        "common_uses": "Relief and prevention of heartburn, acid indigestion, and peptic ulcer treatment.",
        "general_precautions": "Take 15 to 60 minutes before eating food or drinking beverages that cause heartburn.",
        "common_side_effects": "Headache, dizziness, constipation, mild diarrhea.",
        "warnings": "Note: Old Ranitidine was largely replaced globally with Famotidine due to NDMA impurity alerts. Use Famotidine for safe H2 acid blockade.",
        "storage_info": "Store at room temperature in a dry place.",
        "dosage_forms": "Tablet (10mg, 20mg, 40mg), Oral Suspension",
        "prescription_required": 0,
        "fda_ndc": "10158-100"
    },
    {
        "name": "Ondansetron",
        "generic_name": "Ondansetron Hydrochloride",
        "brand_names": "Zofran, Emeset, Ondem",
        "manufacturer": "Novartis / Cipla",
        "category": "Antiemetic (5-HT3 Receptor Antagonist)",
        "common_uses": "Prevention of nausea and vomiting associated with cancer chemotherapy, radiation therapy, and post-operative recovery.",
        "general_precautions": "Orally disintegrating tablets should be dissolved on top of the tongue without chewing.",
        "common_side_effects": "Headache, constipation, sensation of warmth or flushing, fatigue.",
        "warnings": "Can cause dose-dependent QT interval prolongation; use caution in patients with underlying cardiac arrhythmias.",
        "storage_info": "Store at 20°C to 25°C protected from light.",
        "dosage_forms": "Oral disintegrating tablet (ODT 4mg, 8mg), Film-coated tablet, IV Ampoule",
        "prescription_required": 1,
        "fda_ndc": "0173-0442"
    },
    {
        "name": "Domperidone",
        "generic_name": "Domperidone",
        "brand_names": "Motilium, Vomistop",
        "manufacturer": "Janssen / Cipla",
        "category": "Prokinetic & Antiemetic (Dopamine Antagonist)",
        "common_uses": "Symptom relief of nausea, vomiting, feeling of fullness, upper abdominal discomfort, and regurgitation.",
        "general_precautions": "Take 15-30 minutes before meals. Use the lowest effective dose for the shortest duration.",
        "common_side_effects": "Dry mouth, mild headache, abdominal cramps.",
        "warnings": "Associated with an increased risk of serious ventricular arrhythmias or sudden cardiac death, particularly in patients >60 years old.",
        "storage_info": "Store below 30°C in a dry place.",
        "dosage_forms": "Tablet (10mg), Suspension, Drops",
        "prescription_required": 1,
        "fda_ndc": "N/A (Non-US/International)"
    },

    # 6. Respiratory & Allergy
    {
        "name": "Cetirizine",
        "generic_name": "Cetirizine Hydrochloride",
        "brand_names": "Zyrtec, Cetzine, Alerid",
        "manufacturer": "Johnson & Johnson / Cipla",
        "category": "Antihistamine (Second-Generation H1)",
        "common_uses": "Relief of allergy symptoms: sneezing, runny nose, itchy/watery eyes, allergic rhinitis, and chronic urticaria (hives).",
        "general_precautions": "Although less sedating than 1st-generation antihistamines, it may still cause drowsiness in some individuals. Avoid alcohol.",
        "common_side_effects": "Drowsiness, fatigue, dry mouth, mild dizziness, sore throat.",
        "warnings": "Exercise caution when operating heavy machinery or driving until you understand how this drug affects your alertness.",
        "storage_info": "Store at 20°C to 25°C. Protect from high humidity.",
        "dosage_forms": "Tablet (5mg, 10mg), Chewable tablet, Syrup (5mg/5mL)",
        "prescription_required": 0,
        "fda_ndc": "50580-726"
    },
    {
        "name": "Montelukast",
        "generic_name": "Montelukast Sodium",
        "brand_names": "Singulair, Montair, Telekast",
        "manufacturer": "Organon / Sun Pharma",
        "category": "Leukotriene Receptor Antagonist (LTRA)",
        "common_uses": "Chronic maintenance treatment of asthma, prevention of exercise-induced bronchospasm, and relief of allergic rhinitis.",
        "general_precautions": "Not intended to treat acute, sudden asthma attacks (keep a rescue inhaler handy). Take in the evening for asthma.",
        "common_side_effects": "Headache, stomach pain, sore throat, mild cough.",
        "warnings": "Black Box Warning: Serious neuropsychiatric events (agitation, depression, sleep disturbances, suicidal thoughts or behaviors). Report any mood changes immediately.",
        "storage_info": "Store at 20°C to 25°C in the original packaging away from light and moisture.",
        "dosage_forms": "Film-coated tablet (10mg), Chewable tablet (4mg, 5mg), Oral Granules",
        "prescription_required": 1,
        "fda_ndc": "0006-0711"
    },
    {
        "name": "Salbutamol",
        "generic_name": "Albuterol / Salbutamol Sulfate",
        "brand_names": "Ventolin, ProAir, Asthalin",
        "manufacturer": "GSK / Teva / Cipla",
        "category": "Bronchodilator (Short-Acting Beta-2 Agonist)",
        "common_uses": "Rapid relief and prevention of bronchospasm in asthma, COPD, and exercise-induced asthma attacks.",
        "general_precautions": "Rinse mouth after use. If using more than 2-3 times per week for acute symptoms, consult a physician for asthma control review.",
        "common_side_effects": "Tremors (shaky hands), nervousness, tachycardia (rapid heart rate), headache.",
        "warnings": "Excessive use indicates poorly controlled asthma and can precipitate severe paradoxically worsening bronchospasm.",
        "storage_info": "Store inhaler between 15°C and 25°C. Do not puncture or incinerate canister.",
        "dosage_forms": "Metered Dose Inhaler (100mcg/puff), Nebulizer solution, Syrup",
        "prescription_required": 1,
        "fda_ndc": "0173-0682"
    },
    {
        "name": "Budesonide",
        "generic_name": "Budesonide",
        "brand_names": "Pulmicort, Budecort, Rhinocort",
        "manufacturer": "AstraZeneca / Cipla",
        "category": "Inhaled Corticosteroid (ICS)",
        "common_uses": "Maintenance treatment of asthma, allergic rhinitis, and Crohn's disease.",
        "general_precautions": "Rinse mouth with water and spit it out after each inhalation to prevent oral candidiasis (thrush) and hoarseness.",
        "common_side_effects": "Throat irritation, hoarseness, cough, dry mouth.",
        "warnings": "Not a rescue medication for acute bronchospasm. Long-term high doses may cause adrenal suppression.",
        "storage_info": "Store upright between 20°C and 25°C.",
        "dosage_forms": "Inhalation Suspension (Respules 0.5mg/2mL), Inhaler, Nasal Spray",
        "prescription_required": 1,
        "fda_ndc": "0186-0388"
    },
    {
        "name": "Fexofenadine",
        "generic_name": "Fexofenadine Hydrochloride",
        "brand_names": "Allegra, Allegix, Fexova",
        "manufacturer": "Sanofi / Torrent",
        "category": "Antihistamine (Non-sedating Second-Generation)",
        "common_uses": "Seasonal allergic rhinitis (hay fever) and chronic idiopathic urticaria.",
        "general_precautions": "Take with water; do not take with fruit juices (grapefruit, apple, orange) as they significantly reduce drug absorption.",
        "common_side_effects": "Headache, back pain, dizziness, mild nausea.",
        "warnings": "Safe non-sedating profile, but caution in severe renal dysfunction.",
        "storage_info": "Store at 20°C to 25°C.",
        "dosage_forms": "Tablet (30mg, 60mg, 120mg, 180mg), Oral Suspension",
        "prescription_required": 0,
        "fda_ndc": "0024-5720"
    },

    # 7. Central Nervous System & Psychiatric
    {
        "name": "Alprazolam",
        "generic_name": "Alprazolam",
        "brand_names": "Xanax, Restyl, Alzolam",
        "manufacturer": "Pfizer / Sun Pharma",
        "category": "Benzodiazepine (Anxiolytic)",
        "common_uses": "Acute short-term management of generalized anxiety disorder (GAD) and panic disorders with or without agoraphobia.",
        "general_precautions": "Controlled substance. High potential for dependence, tolerance, and physical withdrawal symptoms upon discontinuation.",
        "common_side_effects": "Drowsiness, lightheadedness, impaired coordination, memory impairment, slurred speech.",
        "warnings": "Black Box Warning: Concomitant use with opioids or alcohol may result in profound sedation, respiratory depression, coma, and death.",
        "storage_info": "Store in a secure, locked medication box at room temperature (20°C to 25°C).",
        "dosage_forms": "Tablet (0.25mg, 0.5mg, 1mg, 2mg), Extended-Release (XR)",
        "prescription_required": 1,
        "fda_ndc": "0009-0029"
    },
    {
        "name": "Sertraline",
        "generic_name": "Sertraline Hydrochloride",
        "brand_names": "Zoloft, Daxid, Serta",
        "manufacturer": "Pfizer / Sun Pharma",
        "category": "Antidepressant (SSRI)",
        "common_uses": "Major depressive disorder (MDD), obsessive-compulsive disorder (OCD), panic disorder, PTSD, social anxiety disorder.",
        "general_precautions": "May take 2 to 4 weeks to notice significant therapeutic benefits. Do not stop abruptly to avoid antidepressant discontinuation syndrome.",
        "common_side_effects": "Nausea, diarrhea, insomnia, sexual dysfunction, tremors, dry mouth.",
        "warnings": "Black Box Warning: Increased risk of suicidal thoughts and behaviors in children, adolescents, and young adults (under 24 years). Risk of Serotonin Syndrome.",
        "storage_info": "Store at 20°C to 25°C in a dry area.",
        "dosage_forms": "Tablet (25mg, 50mg, 100mg), Oral Solution (20mg/mL)",
        "prescription_required": 1,
        "fda_ndc": "0049-4960"
    },
    {
        "name": "Escitalopram",
        "generic_name": "Escitalopram Oxalate",
        "brand_names": "Lexapro, Cipralex, Nexito",
        "manufacturer": "AbbVie / Lundbeck / Sun Pharma",
        "category": "Antidepressant (SSRI)",
        "common_uses": "Treatment of major depressive disorder and generalized anxiety disorder.",
        "general_precautions": "Take once daily in morning or evening. Avoid alcohol consumption.",
        "common_side_effects": "Insomnia, ejaculation disorder, nausea, increased sweating, fatigue.",
        "warnings": "Black Box Warning: Suicidality risk in adolescents/young adults. Dose-dependent QT prolongation.",
        "storage_info": "Store at 20°C to 25°C.",
        "dosage_forms": "Tablet (5mg, 10mg, 20mg), Oral Solution",
        "prescription_required": 1,
        "fda_ndc": "0456-2010"
    },
    {
        "name": "Gabapentin",
        "generic_name": "Gabapentin",
        "brand_names": "Neurontin, Gaba, Gabapin",
        "manufacturer": "Pfizer / Intas",
        "category": "Anticonvulsant & Neuropathic Pain Agent",
        "common_uses": "Postherpetic neuralgia (shingles nerve pain), diabetic peripheral neuropathy, and adjunctive therapy for partial-onset seizures.",
        "general_precautions": "Do not discontinue abruptly due to risk of increased seizure frequency. Avoid taking within 2 hours of antacids.",
        "common_side_effects": "Dizziness, somnolence, peripheral edema, ataxia (unsteady gait), fatigue.",
        "warnings": "Respiratory depression risk when combined with CNS depressants or in patients with compromised respiratory function.",
        "storage_info": "Store at 25°C.",
        "dosage_forms": "Capsule (100mg, 300mg, 400mg), Tablet (600mg, 800mg), Solution",
        "prescription_required": 1,
        "fda_ndc": "0071-0803"
    },
    {
        "name": "Pregabalin",
        "generic_name": "Pregabalin",
        "brand_names": "Lyrica, Pregabid, Maxgalin",
        "manufacturer": "Pfizer / Sun Pharma",
        "category": "Anticonvulsant & Neuropathic Pain Agent",
        "common_uses": "Neuropathic pain associated with diabetic peripheral neuropathy, spinal cord injury, postherpetic neuralgia, and fibromyalgia.",
        "general_precautions": "Taper gradually when discontinuing. May cause weight gain and peripheral edema.",
        "common_side_effects": "Dizziness, drowsiness, dry mouth, blurred vision, weight gain.",
        "warnings": "Controlled substance with potential for misuse and psychological dependence.",
        "storage_info": "Store at 25°C.",
        "dosage_forms": "Capsule (25mg, 50mg, 75mg, 150mg, 300mg)",
        "prescription_required": 1,
        "fda_ndc": "0071-1014"
    },
    {
        "name": "Clonazepam",
        "generic_name": "Clonazepam",
        "brand_names": "Klonopin, Rivotril, Clonafit",
        "manufacturer": "Roche / Torrent",
        "category": "Benzodiazepine (Anticonvulsant & Anxiolytic)",
        "common_uses": "Panic disorder, seizure disorders (Lennox-Gastaut, myoclonic, akinetic), and akathisia.",
        "general_precautions": "High dependence liability; avoid sudden discontinuation. Avoid alcohol and driving.",
        "common_side_effects": "Sedation, ataxia, cognitive impairment, muscle weakness.",
        "warnings": "Concomitant use with opioids may cause fatal respiratory arrest.",
        "storage_info": "Store at 25°C in a secure place.",
        "dosage_forms": "Tablet (0.5mg, 1mg, 2mg), Orally Disintegrating Tablet",
        "prescription_required": 1,
        "fda_ndc": "0004-0058"
    },

    # 8. Anti-inflammatory, Corticosteroids & Antigout
    {
        "name": "Prednisolone",
        "generic_name": "Prednisolone / Prednisone",
        "brand_names": "Deltasone, Omnipred, Wysolone",
        "manufacturer": "Pfizer / Wyeth",
        "category": "Systemic Corticosteroid",
        "common_uses": "Severe inflammatory conditions, acute asthma exacerbation, autoimmune disorders (rheumatoid arthritis, lupus), severe allergic reactions.",
        "general_precautions": "Take with food in the morning to match natural cortisol rhythms. Do not stop abruptly after prolonged use (requires gradual tapering).",
        "common_side_effects": "Increased appetite, insomnia, fluid retention, mood swings, elevated blood glucose.",
        "warnings": "Prolonged therapy causes immunosuppression, Cushingoid features, osteoporosis, cataracts, and hypothalamic-pituitary-adrenal (HPA) axis suppression.",
        "storage_info": "Store at 15°C to 30°C in a light-resistant container.",
        "dosage_forms": "Tablet (5mg, 10mg, 20mg, 40mg), Oral Syrup, Ophthalmic Suspension",
        "prescription_required": 1,
        "fda_ndc": "0054-4728"
    },
    {
        "name": "Dexamethasone",
        "generic_name": "Dexamethasone",
        "brand_names": "Decadron, Dexona, Maxidex",
        "manufacturer": "Merck / Zydus",
        "category": "Potent Systemic Corticosteroid",
        "common_uses": "Severe allergic reactions, cerebral edema, severe COVID-19 respiratory distress, anti-inflammatory treatment.",
        "general_precautions": "Short-term high potency steroid. Monitor blood sugar in diabetic patients.",
        "common_side_effects": "Hyperglycemia, sleep disturbance, gastrointestinal upset, anxiety.",
        "warnings": "Immunosuppression increases susceptibility to secondary bacterial or fungal infections.",
        "storage_info": "Store at 20°C to 25°C.",
        "dosage_forms": "Tablet (0.5mg, 2mg, 4mg, 8mg), Injection (4mg/mL)",
        "prescription_required": 1,
        "fda_ndc": "0006-0041"
    },
    {
        "name": "Allopurinol",
        "generic_name": "Allopurinol",
        "brand_names": "Zyloprim, Aluron, Zyloric",
        "manufacturer": "GSK / RPG Life Sciences",
        "category": "Xanthine Oxidase Inhibitor (Antigout)",
        "common_uses": "Prevention of gout attacks, hyperuricemia, and uric acid kidney stones.",
        "general_precautions": "Do not start during an acute gout attack. Drink plenty of water (at least 2-3 liters daily).",
        "common_side_effects": "Skin rash, diarrhea, nausea, mild elevation of liver enzymes.",
        "warnings": "Discontinue at first sign of skin rash due to risk of rare, life-threatening Stevens-Johnson Syndrome (SJS) or DRESS syndrome.",
        "storage_info": "Store at 20°C to 25°C in a dry area.",
        "dosage_forms": "Tablet (100mg, 300mg)",
        "prescription_required": 1,
        "fda_ndc": "0093-0145"
    },
    # 9. Additional Essential Medications
    {
        "name": "Digoxin",
        "generic_name": "Digoxin",
        "brand_names": "Lanoxin, Digitek",
        "manufacturer": "GSK / Mylan",
        "category": "Cardiac Glycoside",
        "common_uses": "Treatment of mild to moderate heart failure and rate control in chronic atrial fibrillation.",
        "general_precautions": "Very narrow therapeutic window (0.5 to 0.9 ng/mL). Monitor renal function, serum potassium, and magnesium closely.",
        "common_side_effects": "Anorexia, nausea, vomiting, visual disturbances (yellow-green halo vision), headache.",
        "warnings": "Black Box Warning: High toxicity risk. Hypokalemia increases susceptibility to digitalis toxicity and fatal arrhythmias.",
        "storage_info": "Store at 25°C protected from light.",
        "dosage_forms": "Tablet (0.125mg, 0.25mg), Pediatric Elixir, IV",
        "prescription_required": 1,
        "fda_ndc": "0173-0242"
    },
    {
        "name": "Spironolactone",
        "generic_name": "Spironolactone",
        "brand_names": "Aldactone, Spiractin",
        "manufacturer": "Pfizer / RPG",
        "category": "Potassium-Sparing Diuretic / Aldosterone Antagonist",
        "common_uses": "Heart failure with reduced ejection fraction, resistant hypertension, cirrhosis edema, and primary hyperaldosteronism.",
        "general_precautions": "Avoid high-potassium foods (bananas, oranges, potassium salt substitutes). Check electrolytes regularly.",
        "common_side_effects": "Hyperkalemia, gynecomastia (breast enlargement in males), menstrual irregularities.",
        "warnings": "Black Box Warning: Tumorigenic in animal studies; avoid unnecessary off-label use.",
        "storage_info": "Store below 25°C.",
        "dosage_forms": "Tablet (25mg, 50mg, 100mg)",
        "prescription_required": 1,
        "fda_ndc": "0025-1001"
    },
    {
        "name": "Lithium",
        "generic_name": "Lithium Carbonate",
        "brand_names": "Lithobid, Eskalith",
        "manufacturer": "Promius / Sun Pharma",
        "category": "Mood Stabilizer",
        "common_uses": "Maintenance and acute manic episodes in Bipolar I disorder.",
        "general_precautions": "Maintain adequate fluid and sodium intake. Regular serum lithium level monitoring is mandatory.",
        "common_side_effects": "Fine hand tremor, polyuria, polydipsia, weight gain, metallic taste.",
        "warnings": "Black Box Warning: Lithium toxicity is closely related to serum levels and can occur at doses close to therapeutic levels.",
        "storage_info": "Store at 20°C to 25°C in tight containers.",
        "dosage_forms": "Capsule (150mg, 300mg, 600mg), Extended-Release Tablet",
        "prescription_required": 1,
        "fda_ndc": "0048-0382"
    },
    {
        "name": "Levofloxacin",
        "generic_name": "Levofloxacin",
        "brand_names": "Levaquin, L-Cin, Glevo",
        "manufacturer": "Janssen / Glenmark",
        "category": "Fluoroquinolone Antibiotic",
        "common_uses": "Pneumonia, acute bacterial sinusitis, skin infections, complicated urinary tract infections.",
        "general_precautions": "Drink plenty of water. Separate from multivalent cations (iron, magnesium, aluminum, zinc).",
        "common_side_effects": "Nausea, headache, dizziness, diarrhea, insomnia.",
        "warnings": "Black Box Warning: Tendinitis, tendon rupture, peripheral neuropathy, and central nervous system effects.",
        "storage_info": "Store at 20°C to 25°C.",
        "dosage_forms": "Tablet (250mg, 500mg, 750mg), IV Solution, Ophthalmic drops",
        "prescription_required": 1,
        "fda_ndc": "0045-1525"
    },
    {
        "name": "Clotrimazole",
        "generic_name": "Clotrimazole",
        "brand_names": "Canesten, Lotrimin, Candid",
        "manufacturer": "Bayer / Glenmark",
        "category": "Antifungal (Azole)",
        "common_uses": "Topical and mucosal fungal infections: athlete's foot (tinea pedis), ringworm, oral thrush, and vaginal candidiasis.",
        "general_precautions": "For external use or specific vaginal/oral troche formulations only. Continue treatment for full recommended duration.",
        "common_side_effects": "Local redness, mild burning sensation, irritation, peeling.",
        "warnings": "Not for ophthalmic use. Discontinue if severe allergic contact dermatitis occurs.",
        "storage_info": "Store at 20°C to 25°C. Avoid freezing.",
        "dosage_forms": "Topical Cream (1%), Lozenges (Troches 10mg), Vaginal Suppository",
        "prescription_required": 0,
        "fda_ndc": "0085-0610"
    },
    {
        "name": "Metronidazole",
        "generic_name": "Metronidazole",
        "brand_names": "Flagyl, Metrogyl",
        "manufacturer": "Pfizer / JB Chemicals",
        "category": "Nitroimidazole Antimicrobial & Antiprotozoal",
        "common_uses": "Anaerobic bacterial infections, bacterial vaginosis, trichomoniasis, giardiasis, and amoebic dysentery.",
        "general_precautions": "Strictly NO ALCOHOL during therapy and for at least 48 hours after the last dose (causes disulfiram-like reaction).",
        "common_side_effects": "Metallic taste, dark reddish-brown urine, nausea, dry mouth.",
        "warnings": "Black Box Warning: Carcinogenic in rodent studies; avoid unnecessary long-term usage.",
        "storage_info": "Store below 25°C protected from light.",
        "dosage_forms": "Tablet (250mg, 400mg, 500mg), Topical Gel, IV Infusion",
        "prescription_required": 1,
        "fda_ndc": "0025-1821"
    },
    {
        "name": "Insulin Glargine",
        "generic_name": "Insulin Glargine (rDNA origin)",
        "brand_names": "Lantus, Basaglar, Toujeo",
        "manufacturer": "Sanofi / Eli Lilly",
        "category": "Long-Acting Basal Insulin",
        "common_uses": "Improvement of glycemic control in adults and children with Type 1 or Type 2 Diabetes Mellitus.",
        "general_precautions": "Administer subcutaneously once daily at the same time every day. Never mix or dilute with any other insulin.",
        "common_side_effects": "Hypoglycemia, weight gain, injection site lipodystrophy or itching.",
        "warnings": "Hypoglycemia is the most common adverse reaction. Do not share injection pens between individuals.",
        "storage_info": "Unopened: Refrigerator (2°C-8°C). In-use pen/vial: Room temperature (<30°C) for up to 28 days.",
        "dosage_forms": "Subcutaneous Solostar Pen (100 units/mL, 300 units/mL), 10mL Vial",
        "prescription_required": 1,
        "fda_ndc": "0024-5860"
    },
    {
        "name": "Pantoprazole",
        "generic_name": "Pantoprazole Sodium",
        "brand_names": "Protonix, Pan 40, Pantocid",
        "manufacturer": "Pfizer / Alkem",
        "category": "Proton Pump Inhibitor (PPI)",
        "common_uses": "Short-term treatment of erosive esophagitis associated with GERD and Zollinger-Ellison syndrome.",
        "general_precautions": "Take 30 minutes before the morning meal. Do not chew or crush delayed-release tablets.",
        "common_side_effects": "Headache, diarrhea, nausea, dizziness.",
        "warnings": "Prolonged use can lead to hypomagnesemia and vitamin B12 malabsorption.",
        "storage_info": "Store at 20°C to 25°C.",
        "dosage_forms": "Delayed-release tablet (20mg, 40mg), IV Injection (40mg)",
        "prescription_required": 0,
        "fda_ndc": "0008-0841"
    }
]

INTERACTIONS_DATA = [
    {
        "drug_a": "Digoxin",
        "drug_b": "Amiodarone",
        "severity": "Major",
        "description": "Amiodarone inhibits P-glycoprotein efflux of Digoxin, increasing serum Digoxin concentrations by 70% to 100% and triggering severe digoxin toxicity (arrhythmias, heart block).",
        "recommendation": "Reduce Digoxin dosage by 50% when initiating Amiodarone and closely monitor serum Digoxin levels and ECG."
    },
    {
        "drug_a": "Digoxin",
        "drug_b": "Furosemide",
        "severity": "Moderate",
        "description": "Furosemide-induced hypokalemia (low potassium) sensitizes the myocardium to Digoxin, greatly heightening the risk of fatal digitalis arrhythmias.",
        "recommendation": "Monitor potassium and magnesium levels regularly. Potassium supplements or sparing agents are often indicated."
    },
    {
        "drug_a": "Lithium",
        "drug_b": "Ibuprofen",
        "severity": "Major",
        "description": "NSAIDs like Ibuprofen reduce renal prostaglandin synthesis, decreasing lithium excretion and causing dangerous toxic lithium accumulation.",
        "recommendation": "Avoid NSAIDs in patients taking Lithium. Use Paracetamol for pain relief instead, and monitor serum lithium levels."
    },
    {
        "drug_a": "Metronidazole",
        "drug_b": "Alcohol",
        "severity": "Major",
        "description": "Metronidazole inhibits acetaldehyde dehydrogenase. Combining with alcohol triggers a violent disulfiram-like reaction (severe nausea, vomiting, tachycardia, throbbing headache, flushing).",
        "recommendation": "Completely abstain from alcoholic beverages and alcohol-containing cough syrups during treatment and for 48 hours afterward."
    },
    {
        "drug_a": "Levofloxacin",
        "drug_b": "Prednisolone",
        "severity": "Major",
        "description": "Concurrent use of fluoroquinolones (Levofloxacin) and systemic corticosteroids dramatically elevates the hazard of Achilles tendinitis and sudden tendon rupture.",
        "recommendation": "Avoid simultaneous therapy where possible. Advise patient to discontinue immediately and rest if any joint or tendon stiffness/pain appears."
    },
    {
        "drug_a": "Insulin Glargine",
        "drug_b": "Metoprolol",
        "severity": "Moderate",
        "description": "Beta-blockers like Metoprolol can mask early sympathetic warning signs of hypoglycemia (tremor, tachycardia, palpitations) except for diaphoresis (sweating).",
        "recommendation": "Educate diabetic patients that sweating may be the only warning sign of low blood sugar while on beta-blockers. Monitor glucose frequently."
    },
    {
        "drug_a": "Spironolactone",
        "drug_b": "Losartan",
        "severity": "Major",
        "description": "Combining ARBs (Losartan) with potassium-sparing diuretics (Spironolactone) creates an additive risk of life-threatening hyperkalemia.",
        "recommendation": "Perform baseline and routine monitoring of serum potassium and creatinine. Restrict dietary potassium supplements."
    },
    {
        "drug_a": "Aspirin",
        "drug_b": "Warfarin",
        "severity": "Major",
        "description": "Concurrent use of Aspirin (an antiplatelet agent) with Warfarin (an anticoagulant) produces a synergistic effect that dramatically amplifies the risk of major gastrointestinal and systemic bleeding.",
        "recommendation": "Avoid combination unless specifically directed and monitored by a cardiologist/hematologist with frequent INR checks. Seek immediate medical attention if unusual bleeding or dark stools occur."
    },
    {
        "drug_a": "Ibuprofen",
        "drug_b": "Lisinopril",
        "severity": "Moderate",
        "description": "NSAIDs like Ibuprofen can diminish the antihypertensive effect of ACE inhibitors like Lisinopril, and the combination significantly increases the risk of acute renal impairment and hyperkalemia (high potassium).",
        "recommendation": "Monitor blood pressure and kidney function. Consider Paracetamol as an alternative for pain relief when taking ACE inhibitors."
    },
    {
        "drug_a": "Metformin",
        "drug_b": "Alcohol",
        "severity": "Major",
        "description": "Excessive acute or chronic alcohol intake potentiates the effect of Metformin on lactate metabolism, significantly elevating the risk of life-threatening Lactic Acidosis and severe hypoglycemia.",
        "recommendation": "Strictly limit or avoid alcohol consumption while taking Metformin. Never binge drink."
    },
    {
        "drug_a": "Omeprazole",
        "drug_b": "Clopidogrel",
        "severity": "Major",
        "description": "Omeprazole competitively inhibits the CYP2C19 liver enzyme required to bioactivate Clopidogrel (Plavix), thereby reducing its antiplatelet effectiveness and increasing the risk of stent thrombosis or heart attack.",
        "recommendation": "Consult physician for safer alternatives such as Pantoprazole or H2 blockers (Famotidine) that have minimal CYP2C19 inhibition."
    },
    {
        "drug_a": "Sertraline",
        "drug_b": "Tramadol",
        "severity": "Major",
        "description": "Both Sertraline (an SSRI) and Tramadol (an opioid with serotonin reuptake inhibition) elevate synaptic serotonin levels, greatly increasing the risk of potentially fatal Serotonin Syndrome and seizures.",
        "recommendation": "Avoid concurrent use. Watch for symptoms of Serotonin Syndrome: agitation, tremor, hyperreflexia, sweating, dilated pupils, and high fever."
    },
    {
        "drug_a": "Alprazolam",
        "drug_b": "Tramadol",
        "severity": "Major",
        "description": "Combining benzodiazepines (Alprazolam) with opioids (Tramadol) causes additive Central Nervous System and respiratory depression, which can lead to profound sedation, coma, or respiratory arrest.",
        "recommendation": "Strictly avoid concomitant use unless under specialized palliative/pain care with close monitoring. Never combine with alcohol."
    },
    {
        "drug_a": "Azithromycin",
        "drug_b": "Amiodarone",
        "severity": "Major",
        "description": "Both drugs prolong the cardiac QT interval. Combined administration markedly increases the hazard of Torsades de Pointes and fatal ventricular arrhythmias.",
        "recommendation": "Avoid combination. Continuous ECG monitoring required if co-administration is clinically unavoidable."
    },
    {
        "drug_a": "Ciprofloxacin",
        "drug_b": "Prednisolone",
        "severity": "Major",
        "description": "Co-administration of fluoroquinolones (Ciprofloxacin) and systemic corticosteroids (Prednisolone) synergistically increases the risk of severe tendinitis and tendon rupture, particularly in the Achilles tendon.",
        "recommendation": "Avoid simultaneous use, especially in patients over 60. Discontinue immediately if pain, swelling, or inflammation occurs in any tendon."
    },
    {
        "drug_a": "Atorvastatin",
        "drug_b": "Clarithromycin",
        "severity": "Major",
        "description": "Clarithromycin is a potent CYP3A4 inhibitor that blocks the metabolism of Atorvastatin, causing high statin blood levels and a high risk of rhabdomyolysis (muscle breakdown) and acute renal failure.",
        "recommendation": "Temporarily withhold Atorvastatin during macrolide antibiotic therapy or switch to an antibiotic that does not inhibit CYP3A4."
    },
    {
        "drug_a": "Doxycycline",
        "drug_b": "Antacids",
        "severity": "Moderate",
        "description": "Antacids containing aluminum, calcium, or magnesium bind to Doxycycline in the gastrointestinal tract, forming insoluble chelates that severely impair antibiotic absorption.",
        "recommendation": "Take Doxycycline at least 2 hours before or 4 hours after taking antacids or mineral supplements."
    },
    {
        "drug_a": "Levothyroxine",
        "drug_b": "Calcium Carbonate",
        "severity": "Moderate",
        "description": "Calcium supplements bind to Levothyroxine in the gut, reducing thyroid hormone bioavailability and resulting in uncontrolled hypothyroidism.",
        "recommendation": "Separate the ingestion of Levothyroxine and calcium/iron supplements by at least 4 hours."
    },
    {
        "drug_a": "Ibuprofen",
        "drug_b": "Aspirin",
        "severity": "Moderate",
        "description": "Ibuprofen interferes with the antiplatelet cardioprotective effect of low-dose Aspirin when taken prior to Aspirin, and the combination substantially increases GI ulceration risk.",
        "recommendation": "Take immediate-release Aspirin at least 30 minutes before Ibuprofen, or take Ibuprofen at least 8 hours before Aspirin."
    },
    {
        "drug_a": "Warfarin",
        "drug_b": "Ciprofloxacin",
        "severity": "Major",
        "description": "Ciprofloxacin inhibits Warfarin metabolism and alters gut flora producing Vitamin K, leading to severe elevation of INR and high risk of life-threatening bleeding.",
        "recommendation": "Frequent INR monitoring is mandatory if antibiotic course is required. Dosage of Warfarin usually requires empiric reduction."
    },
    {
        "drug_a": "Allopurinol",
        "drug_b": "Amoxicillin",
        "severity": "Moderate",
        "description": "Concomitant administration of Allopurinol and Amoxicillin significantly increases the incidence of erythematous and maculopapular skin rashes.",
        "recommendation": "Monitor closely for rashes and seek medical advice if skin eruptions develop."
    },
    {
        "drug_a": "Lisinopril",
        "drug_b": "Spironolactone",
        "severity": "Major",
        "description": "Combining ACE inhibitors (Lisinopril) with potassium-sparing diuretics (Spironolactone) causes severe hyperkalemia, potentially inducing fatal cardiac arrhythmias.",
        "recommendation": "Check serum potassium and renal panel regularly. Avoid high-potassium diets or salt substitutes."
    },
    {
        "drug_a": "Paracetamol",
        "drug_b": "Warfarin",
        "severity": "Minor",
        "description": "Chronic regular daily intake of high-dose Paracetamol (>2g/day for multiple days) may moderately augment the anticoagulant effect of Warfarin and slightly increase INR.",
        "recommendation": "Occasional or single doses of Paracetamol are generally safe. Monitor INR if taking paracetamol regularly for several consecutive days."
    },
    {
        "drug_a": "Cetirizine",
        "drug_b": "Alprazolam",
        "severity": "Moderate",
        "description": "Concurrent use of antihistamines and benzodiazepines enhances central nervous system depression, leading to severe somnolence, slowed reflexes, and impaired psychomotor coordination.",
        "recommendation": "Avoid driving or operating dangerous equipment. Do not consume alcohol."
    },
    {
        "drug_a": "Metoprolol",
        "drug_b": "Amlodipine",
        "severity": "Minor",
        "description": "Both medications lower blood pressure through complementary mechanisms (beta-blockade and calcium channel blockade). May cause additive hypotension or bradycardia.",
        "recommendation": "Commonly prescribed together under physician supervision. Monitor resting blood pressure and pulse rate."
    },
    {
        "drug_a": "Furosemide",
        "drug_b": "Gentamicin",
        "severity": "Major",
        "description": "Co-administration of loop diuretics with aminoglycoside antibiotics potentiates ototoxicity (permanent hearing loss) and nephrotoxicity.",
        "recommendation": "Avoid combination. Monitor renal function and hearing acuity if co-treatment is unavoidable."
    },
    {
        "drug_a": "Colchicine",
        "drug_b": "Clarithromycin",
        "severity": "Major",
        "description": "Clarithromycin strongly inhibits CYP3A4 and P-glycoprotein, triggering dangerous accumulation of Colchicine with severe multi-organ toxicity.",
        "recommendation": "Co-administration is contraindicated, particularly in patients with renal or hepatic impairment."
    }
]

def seed_database():
    """Populates the SQLite database with initial seed data."""
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Insert medicines
    med_count = 0
    for med in MEDICINES_DATA:
        cur.execute("""
            INSERT INTO medicines (
                name, generic_name, brand_names, manufacturer, category,
                common_uses, general_precautions, common_side_effects,
                warnings, storage_info, dosage_forms, prescription_required, fda_ndc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                generic_name=excluded.generic_name,
                brand_names=excluded.brand_names,
                manufacturer=excluded.manufacturer,
                category=excluded.category,
                common_uses=excluded.common_uses,
                general_precautions=excluded.general_precautions,
                common_side_effects=excluded.common_side_effects,
                warnings=excluded.warnings,
                storage_info=excluded.storage_info,
                dosage_forms=excluded.dosage_forms,
                prescription_required=excluded.prescription_required,
                fda_ndc=excluded.fda_ndc
        """, (
            med["name"], med["generic_name"], med["brand_names"], med["manufacturer"],
            med["category"], med["common_uses"], med["general_precautions"],
            med["common_side_effects"], med["warnings"], med["storage_info"],
            med.get("dosage_forms", "Tablet"), med.get("prescription_required", 0),
            med.get("fda_ndc", "")
        ))
        med_count += 1

    # 2. Insert drug interactions (both forward and reverse pairs)
    interaction_count = 0
    for inter in INTERACTIONS_DATA:
        # Drug A -> Drug B
        cur.execute("""
            INSERT INTO drug_interactions (drug_a, drug_b, severity, description, recommendation)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(drug_a, drug_b) DO UPDATE SET
                severity=excluded.severity,
                description=excluded.description,
                recommendation=excluded.recommendation
        """, (inter["drug_a"], inter["drug_b"], inter["severity"], inter["description"], inter["recommendation"]))
        
        # Drug B -> Drug A (Symmetric)
        cur.execute("""
            INSERT INTO drug_interactions (drug_a, drug_b, severity, description, recommendation)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(drug_a, drug_b) DO UPDATE SET
                severity=excluded.severity,
                description=excluded.description,
                recommendation=excluded.recommendation
        """, (inter["drug_b"], inter["drug_a"], inter["severity"], inter["description"], inter["recommendation"]))
        
        interaction_count += 1

    conn.commit()
    conn.close()
    print(f"Database seeded successfully: {med_count} medicines, {interaction_count} interaction rules.")

if __name__ == "__main__":
    seed_database()
