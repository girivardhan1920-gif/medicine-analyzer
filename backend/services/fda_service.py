"""
OpenFDA Drug Data Integration Service.
Queries official OpenFDA endpoints for drug labels, active ingredients, warnings, and indications.
"""
import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

def query_openfda_by_name(drug_name):
    """
    Queries OpenFDA Drug Label API for a specific brand or generic name.
    Returns structured data or None if not found / network error.
    """
    if not drug_name or len(drug_name.strip()) < 2:
        return None

    clean_name = drug_name.strip()
    # Search in openfda.brand_name OR openfda.generic_name OR openfda.substance_name
    search_query = f'(openfda.brand_name:"{clean_name}"+OR+openfda.generic_name:"{clean_name}"+OR+openfda.substance_name:"{clean_name}")'
    url = f"{Config.OPENFDA_API_BASE}/label.json?search={search_query}&limit=1"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                first_result = results[0]
                openfda_block = first_result.get("openfda", {})
                
                brand_names = openfda_block.get("brand_name", [clean_name])
                generic_names = openfda_block.get("generic_name", [clean_name])
                manufacturers = openfda_block.get("manufacturer_name", ["Verified Pharmaceutical Mfr"])
                
                # Extract sections if available
                indications = first_result.get("indications_and_usage", ["Information not available in label summary."])
                warnings = first_result.get("warnings", ["Consult healthcare professional for specific warnings."])
                adverse_reactions = first_result.get("adverse_reactions", ["Consult package insert for full adverse event profile."])
                storage = first_result.get("storage_and_handling", ["Store at controlled room temperature."])
                precautions = first_result.get("precautions", ["Use under medical supervision."])
                dosage_forms = openfda_block.get("dosage_form", ["Tablet / Capsule"])

                return {
                    "source": "OpenFDA (Live US FDA Data)",
                    "name": brand_names[0] if brand_names else clean_name.title(),
                    "generic_name": generic_names[0] if generic_names else clean_name.title(),
                    "brand_names": ", ".join(brand_names[:5]),
                    "manufacturer": manufacturers[0] if manufacturers else "Standard Pharmaceutical Lab",
                    "category": openfda_block.get("pharm_class_cs", ["Therapeutic Agent"])[0] if openfda_block.get("pharm_class_cs") else "Prescription/OTC Medication",
                    "common_uses": indications[0][:300] if isinstance(indications, list) and indications else str(indications)[:300],
                    "general_precautions": precautions[0][:300] if isinstance(precautions, list) and precautions else str(precautions)[:300],
                    "common_side_effects": adverse_reactions[0][:300] if isinstance(adverse_reactions, list) and adverse_reactions else str(adverse_reactions)[:300],
                    "warnings": warnings[0][:350] if isinstance(warnings, list) and warnings else str(warnings)[:350],
                    "storage_info": storage[0][:200] if isinstance(storage, list) and storage else str(storage)[:200],
                    "dosage_forms": ", ".join(dosage_forms[:3]),
                    "prescription_required": 1 if "prescription" in str(first_result).lower() else 0
                }
    except Exception as e:
        logger.warning(f"OpenFDA query failed for '{drug_name}': {e}")

    return None
