import React, { useState, useEffect } from 'react';
import { 
  Search, 
  ScanLine, 
  Pill, 
  ShieldCheck, 
  Zap, 
  Sparkles, 
  Database, 
  ArrowRight,
  Stethoscope,
  Activity,
  AlertTriangle
} from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';
import { SAMPLE_MEDS_DEMO } from '../services/sampleData';
import { searchMedicines, getDashboardStats } from '../services/api';

export default function HomePage({ onNavigate, onSelectMedicine }) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [stats, setStats] = useState({
    total_medicines: 51,
    known_interactions: 54,
    total_queries_processed: 12,
    therapeutic_categories: 9
  });

  useEffect(() => {
    getDashboardStats()
      .then(res => res.stats && setStats(res.stats))
      .catch(e => console.warn('Could not load stats', e));
  }, []);

  const handleSearchChange = async (e) => {
    const val = e.target.value;
    setQuery(val);
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

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSelectMedicine(query.trim());
  };

  return (
    <div>
      {/* Permanent Medical Disclaimer */}
      <DisclaimerBanner />

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-tag">
          <Sparkles size={16} />
          <span>AI-Powered Medical Intelligence & Safety Platform</span>
        </div>

        <h1 className="hero-title">
          Understand Your Medications in <span>Simple, Clear Language</span>
        </h1>

        <p className="hero-subtitle">
          Instantly recognize prescription labels, identify generic ingredients, evaluate multi-drug 
          interactions, and get safety-grounded answers powered by verified pharmaceutical databases.
        </p>

        {/* Global Live Search Bar */}
        <div className="hero-search-wrapper">
          <form onSubmit={handleSearchSubmit}>
            <div className="search-input-box">
              <Search size={22} color="var(--primary)" style={{ marginRight: '10px' }} />
              <input
                id="main-search-input"
                type="text"
                value={query}
                onChange={handleSearchChange}
                placeholder="Search medicine name (e.g. Paracetamol, Amoxicillin, Metformin, Lipitor)..."
              />
              <button type="submit" className="btn btn-primary btn-sm" style={{ borderRadius: 'var(--radius-full)' }}>
                <span>Analyze</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </form>

          {/* Autocomplete Dropdown */}
          {suggestions.length > 0 && (
            <div className="search-dropdown">
              {suggestions.map((s) => (
                <div
                  key={s.id}
                  className="search-dropdown-item"
                  onClick={() => {
                    setQuery('');
                    setSuggestions([]);
                    onSelectMedicine(s.name);
                  }}
                >
                  <div>
                    <strong style={{ color: 'var(--text-primary)', fontSize: '0.95rem' }}>{s.name}</strong>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginLeft: '8px' }}>
                      ({s.generic_name})
                    </span>
                  </div>
                  <span className="badge badge-primary">{s.category}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Access Featured Pills */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Popular Queries:</span>
          {SAMPLE_MEDS_DEMO.map((med, idx) => (
            <button
              key={idx}
              className="sample-pill"
              onClick={() => onSelectMedicine(med.name)}
            >
              <span>{med.icon} {med.name}</span>
            </button>
          ))}
        </div>
      </section>

      {/* Platform Dashboard Stats Grid */}
      <section className="stats-grid">
        <div className="glass-card stat-card">
          <div className="stat-icon" style={{ background: 'var(--primary-light)', color: 'var(--primary)' }}>
            <Database size={26} />
          </div>
          <div className="stat-info">
            <h3>{stats.total_medicines}+</h3>
            <p>Verified Medicines Indexed</p>
          </div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-icon" style={{ background: 'rgba(225, 29, 72, 0.12)', color: 'var(--accent-rose)' }}>
            <Pill size={26} />
          </div>
          <div className="stat-info">
            <h3>{stats.known_interactions}+</h3>
            <p>Known Drug Interaction Rules</p>
          </div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-icon" style={{ background: 'rgba(13, 148, 136, 0.12)', color: 'var(--accent-teal)' }}>
            <ScanLine size={26} />
          </div>
          <div className="stat-info">
            <h3>OCR / Vision</h3>
            <p>Package Text Recognition</p>
          </div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-icon" style={{ background: 'rgba(217, 119, 6, 0.12)', color: 'var(--accent-amber)' }}>
            <ShieldCheck size={26} />
          </div>
          <div className="stat-info">
            <h3>OpenFDA Grounded</h3>
            <p>Zero AI Hallucinations</p>
          </div>
        </div>
      </section>

      {/* Core Project Features Showcase Grid */}
      <section style={{ marginTop: '20px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h2 style={{ fontSize: '1.85rem', marginBottom: '8px' }}>
            Comprehensive Pharmaceutical Analysis Modules
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', maxWidth: '600px', margin: '0 auto' }}>
            Designed for patients, healthcare students, and researchers to verify drug safety in seconds.
          </p>
        </div>

        <div className="features-grid">
          {/* Feature 1 */}
          <div className="glass-card feature-card glass-card-interactive" onClick={() => onNavigate('analyzer')}>
            <div className="feature-card-icon">
              <ScanLine size={24} />
            </div>
            <h3>Medicine & Image Analyzer</h3>
            <p>
              Search by name or upload a photo of your tablet strip or syrup box. Our OCR engine extracts 
              names and displays layman-friendly breakdowns.
            </p>
            <div style={{ marginTop: '16px', color: 'var(--primary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>Try Analyzer</span> <ArrowRight size={16} />
            </div>
          </div>

          {/* Feature 2 */}
          <div className="glass-card feature-card glass-card-interactive" onClick={() => onNavigate('interactions')}>
            <div className="feature-card-icon" style={{ background: 'rgba(225, 29, 72, 0.12)', color: 'var(--accent-rose)' }}>
              <Pill size={24} />
            </div>
            <h3>Multi-Drug Interaction Checker</h3>
            <p>
              Select two or more medications to test for dangerous drug-drug interactions, synergistic side 
              effects, and clinician consultation recommendations.
            </p>
            <div style={{ marginTop: '16px', color: 'var(--accent-rose)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>Check Interactions</span> <ArrowRight size={16} />
            </div>
          </div>

          {/* Feature 3 */}
          <div className="glass-card feature-card glass-card-interactive" onClick={() => onNavigate('assistant')}>
            <div className="feature-card-icon" style={{ background: 'rgba(13, 148, 136, 0.12)', color: 'var(--accent-teal)' }}>
              <Sparkles size={24} />
            </div>
            <h3>AI Pharmacist Assistant</h3>
            <p>
              Ask questions regarding medicine storage, side effects, precautions, and mechanisms with strict 
              educational safety guardrails and verified data grounding.
            </p>
            <div style={{ marginTop: '16px', color: 'var(--accent-teal)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>Chat with AI</span> <ArrowRight size={16} />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
