"""
Multi-Drug Interaction Analysis Service.
Evaluates pairwise and multi-drug combinations against database rules and clinical severity matrices.
"""
from database.db import query_db

def find_interactions_for_drugs(drug_list):
    """
    Takes a list of medicine names (e.g. ['Aspirin', 'Warfarin', 'Lisinopril']),
    normalizes them, queries interaction rules, and groups by severity.
    """
    if not drug_list or len(drug_list) < 2:
        return {
            "total_interactions": 0,
            "interactions": [],
            "risk_level": "Safe / None Detected",
            "consultation_recommended": False,
            "message": "Please select or enter at least two medications to evaluate interactions."
        }

    # Clean and deduplicate names
    clean_drugs = []
    seen = set()
    for d in drug_list:
        name = d.strip()
        if name and name.lower() not in seen:
            seen.add(name.lower())
            clean_drugs.append(name)

    interactions_found = []
    major_count = 0
    moderate_count = 0
    minor_count = 0

    # Test all pairs
    n = len(clean_drugs)
    for i in range(n):
        for j in range(i + 1, n):
            drug_a = clean_drugs[i]
            drug_b = clean_drugs[j]

            # Query database for (drug_a, drug_b) or (drug_b, drug_a)
            sql = """
                SELECT drug_a, drug_b, severity, description, recommendation
                FROM drug_interactions
                WHERE (LOWER(drug_a) = LOWER(?) AND LOWER(drug_b) = LOWER(?))
                   OR (LOWER(drug_a) = LOWER(?) AND LOWER(drug_b) = LOWER(?))
                   OR (LOWER(drug_a) LIKE LOWER(?) AND LOWER(drug_b) LIKE LOWER(?))
                   OR (LOWER(drug_a) LIKE LOWER(?) AND LOWER(drug_b) LIKE LOWER(?))
            """
            like_a = f"%{drug_a}%"
            like_b = f"%{drug_b}%"
            rows = query_db(sql, (drug_a, drug_b, drug_b, drug_a, like_a, like_b, like_b, like_a))

            if rows:
                for row in rows:
                    severity = row["severity"]
                    if severity == "Major":
                        major_count += 1
                    elif severity == "Moderate":
                        moderate_count += 1
                    else:
                        minor_count += 1

                    interactions_found.append({
                        "drug_a": row["drug_a"],
                        "drug_b": row["drug_b"],
                        "severity": severity,
                        "description": row["description"],
                        "recommendation": row["recommendation"]
                    })

    # Overall risk calculation
    if major_count > 0:
        overall_risk = "HIGH RISK (Major Interactions Detected)"
        consultation = True
    elif moderate_count > 0:
        overall_risk = "MODERATE RISK (Caution Advised)"
        consultation = True
    elif minor_count > 0:
        overall_risk = "LOW RISK (Minor Interaction)"
        consultation = False
    else:
        overall_risk = "NO KNOWN INTERACTIONS IN DATABASE"
        consultation = False

    return {
        "drugs_checked": clean_drugs,
        "total_interactions": len(interactions_found),
        "major_count": major_count,
        "moderate_count": moderate_count,
        "minor_count": minor_count,
        "risk_level": overall_risk,
        "consultation_recommended": consultation,
        "interactions": interactions_found,
        "consultation_message": (
            "⚠️ Potential interaction identified. We strongly advise consulting your doctor or pharmacist "
            "before combining these medications." if consultation else
            "No known clinical interaction found in our verified database. Always confirm with your healthcare provider."
        )
    }
