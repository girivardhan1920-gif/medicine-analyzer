import React, { useState, useEffect } from 'react';
import { 
  Pill, 
  Search, 
  Plus, 
  X, 
  ShieldAlert, 
  AlertTriangle, 
  RefreshCw, 
  Sparkles,
  Stethoscope
} from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';
import InteractionCard from '../components/InteractionCard';
import { checkDrugInteractions, searchMedicines, getCommonInteractionPairs } from '../services/api';

export default function InteractionPage({ preSelectedMeds = [] }) {
  const [selectedDrugs, setSelectedDrugs] = useState(preSelectedMeds.length ? preSelectedMeds : ['Aspirin', 'Warfarin']);
  const [inputVal, setInputVal] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [commonPairs, setCommonPairs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getCommonInteractionPairs().then(res => res.common_combinations && setCommonPairs(res.common_combinations)).catch(console.error);
    // Auto-check on load if we have >= 2 medicines
    if (selectedDrugs.length >= 2) {
      runCheck(selectedDrugs);
    }
  }, []);

  const handleInputChange = async (e) => {
    const val = e.target.value;
    setInputVal(val);
    if (val.trim().length > 1) {
      try {
        const res = await searchMedicines(val.trim());
        setSuggestions(res.results || []);
      } catch (err) {
        setSuggestions([]);
      }
    } else {
      setSuggestions([]);
    }
  };

  const addDrug = (drugName) => {
    const trimmed = drugName.trim();
    if (trimmed && !selectedDrugs.some(d => d.toLowerCase() === trimmed.toLowerCase())) {
      const updated = [...selectedDrugs, trimmed];
      setSelectedDrugs(updated);
      setInputVal('');
      setSuggestions([]);
      if (updated.length >= 2) {
        runCheck(updated);
      }
    }
  };

  const removeDrug = (indexToRemove) => {
    const updated = selectedDrugs.filter((_, idx) => idx !== indexToRemove);
    setSelectedDrugs(updated);
    if (updated.length >= 2) {
      runCheck(updated);
    } else {
      setResult(null);
    }
  };

  const runCheck = async (drugsToCheck) => {
    const targetList = drugsToCheck || selectedDrugs;
    if (targetList.length < 2) {
      setError('Please add at least 2 medicines to evaluate drug interactions.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await checkDrugInteractions(targetList);
      setResult(res.data);
    } catch (err) {
      setError(err.message || 'Failed to check drug interactions.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyPreset = (drugs) => {
    setSelectedDrugs(drugs);
    runCheck(drugs);
  };

  return (
    <div className="interaction-container">
      <DisclaimerBanner />

      <div style={{ textAlign: 'center', marginBottom: '28px' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '6px' }}>Multi-Drug Interaction Checker</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Enter two or more prescription or over-the-counter medications to check for known conflicts and side effect risks.
        </p>
      </div>

      {/* Input Selector Card */}
      <div className="glass-card interaction-input-card">
        <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '12px' }}>
          Selected Medications to Evaluate:
        </h4>

        {/* Selected Drugs Tags */}
        <div className="selected-drugs-pills">
          {selectedDrugs.length === 0 ? (
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              No medicines added yet. Type below to add medications...
            </span>
          ) : (
            selectedDrugs.map((drug, idx) => (
              <span key={idx} className="drug-pill-tag">
                <Pill size={14} />
                <span>{drug}</span>
                <button type="button" onClick={() => removeDrug(idx)} title="Remove medicine">
                  <X size={14} />
                </button>
              </span>
            ))
          )}
        </div>

        {/* Search input to add more */}
        <div style={{ position: 'relative', marginBottom: '16px' }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <div className="search-input-box" style={{ flex: 1 }}>
              <Search size={18} color="var(--primary)" style={{ marginRight: '8px' }} />
              <input
                id="interaction-search-input"
                type="text"
                value={inputVal}
                onChange={handleInputChange}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    if (inputVal.trim()) addDrug(inputVal);
                  }
                }}
                placeholder="Type drug name (e.g. Aspirin, Warfarin, Metformin, Lisinopril) & press Enter..."
              />
            </div>
            <button
              id="interaction-add-btn"
              type="button"
              className="btn btn-secondary"
              onClick={() => inputVal.trim() && addDrug(inputVal)}
              disabled={!inputVal.trim()}
            >
              <Plus size={16} />
              <span>Add</span>
            </button>
          </div>

          {/* Autocomplete Dropdown */}
          {suggestions.length > 0 && (
            <div className="search-dropdown">
              {suggestions.map((s) => (
                <div
                  key={s.id}
                  className="search-dropdown-item"
                  onClick={() => addDrug(s.name)}
                >
                  <div>
                    <strong>{s.name}</strong> <span style={{ color: 'var(--text-muted)' }}>({s.generic_name})</span>
                  </div>
                  <span className="badge badge-teal">{s.category}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Check Button & One-Click Presets */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <button
            id="run-interaction-check-btn"
            className="btn btn-primary"
            onClick={() => runCheck()}
            disabled={loading || selectedDrugs.length < 2}
          >
            {loading ? <RefreshCw className="spin-icon" size={18} /> : <Sparkles size={18} />}
            <span>Evaluate Interactions ({selectedDrugs.length} Drugs)</span>
          </button>

          <button
            className="btn btn-secondary btn-sm"
            onClick={() => { setSelectedDrugs([]); setResult(null); }}
            disabled={selectedDrugs.length === 0}
          >
            Clear All
          </button>
        </div>

        {/* Clinical Demo Scenarios */}
        {commonPairs.length > 0 && (
          <div style={{ marginTop: '24px', paddingTop: '16px', borderTop: '1px solid var(--border-subtle)' }}>
            <h5 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '10px' }}>
              Common Clinical Test Cases (Click to Test):
            </h5>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {commonPairs.map((p, idx) => (
                <button
                  key={idx}
                  type="button"
                  className="sample-pill"
                  onClick={() => handleApplyPreset(p.medicines)}
                >
                  <strong>{p.title}</strong>
                  <span style={{ fontSize: '0.75rem', opacity: 0.8, marginLeft: '6px' }}>
                    ({p.expected_severity})
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Results View */}
      {result && <InteractionCard result={result} />}
    </div>
  );
}
