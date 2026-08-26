/**
 * Sample Demo Data for instant presentation and testing
 */

export const SAMPLE_MEDS_DEMO = [
  {
    name: 'Paracetamol',
    generic: 'Acetaminophen',
    category: 'Analgesic & Antipyretic',
    icon: '💊',
    tagline: 'Fever & Pain Relief'
  },
  {
    name: 'Amoxicillin',
    generic: 'Amoxicillin Trihydrate',
    category: 'Antibiotic (Penicillin)',
    icon: '🔬',
    tagline: 'Bacterial Infection Treatment'
  },
  {
    name: 'Metformin',
    generic: 'Metformin HCl',
    category: 'Antidiabetic (Biguanide)',
    icon: '🩸',
    tagline: 'Blood Sugar Regulation'
  },
  {
    name: 'Atorvastatin',
    generic: 'Atorvastatin Calcium',
    category: 'Statin (Lipid Lowering)',
    icon: '🫀',
    tagline: 'Cholesterol & Heart Health'
  },
  {
    name: 'Omeprazole',
    generic: 'Omeprazole',
    category: 'Proton Pump Inhibitor',
    icon: '🛡️',
    tagline: 'Acid Reflux & GERD'
  },
  {
    name: 'Cetirizine',
    generic: 'Cetirizine HCl',
    category: 'Antihistamine',
    icon: '🌿',
    tagline: 'Allergy & Itch Relief'
  }
];

export const DEMO_INTERACTION_SCENARIOS = [
  {
    name: 'Aspirin + Warfarin',
    severity: 'Major',
    drugs: ['Aspirin', 'Warfarin'],
    summary: 'Extreme Bleeding Risk (Antiplatelet + Anticoagulant)'
  },
  {
    name: 'Ibuprofen + Lisinopril',
    severity: 'Moderate',
    drugs: ['Ibuprofen', 'Lisinopril'],
    summary: 'Reduced BP control & potential renal stress'
  },
  {
    name: 'Metformin + Alcohol',
    severity: 'Major',
    drugs: ['Metformin', 'Alcohol'],
    summary: 'Hazardous Lactic Acidosis risk'
  },
  {
    name: 'Paracetamol + Cetirizine',
    severity: 'Minor / Safe',
    drugs: ['Paracetamol', 'Cetirizine'],
    summary: 'Standard Cold/Fever combo with no major interaction'
  }
];
