import React, { useState, useEffect } from 'react';
import { Pill, Search, Filter, BookOpen, Layers, ArrowRight } from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';
import MedicineCard from '../components/MedicineCard';
import { getFeaturedMedicines, getMedicineCategories, getMedicineByName } from '../services/api';

export default function DetailsPage({ selectedDrug, onSelectDrug, onCheckInteractions }) {
  const [categories, setCategories] = useState([]);
  const [medicines, setMedicines] = useState([]);
  const [activeCategory, setActiveCategory] = useState('All');
  const [loading, setLoading] = useState(false);
  const [selectedMedicineData, setSelectedMedicineData] = useState(null);

  useEffect(() => {
    getMedicineCategories().then(res => res.categories && setCategories(res.categories)).catch(console.error);
    getFeaturedMedicines().then(res => res.featured && setMedicines(res.featured)).catch(console.error);
  }, []);

  useEffect(() => {
    if (selectedDrug) {
      setLoading(true);
      getMedicineByName(selectedDrug)
        .then(res => {
          setSelectedMedicineData(res);
        })
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [selectedDrug]);

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <DisclaimerBanner />

      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '6px' }}>Medicine Pharmacological Compendium</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Browse verified clinical drug monographs, dosage classifications, and precautions.
        </p>
      </div>

      {selectedMedicineData && selectedMedicineData.data ? (
        <div>
          <button 
            className="btn btn-secondary btn-sm" 
            style={{ marginBottom: '16px' }}
            onClick={() => setSelectedMedicineData(null)}
          >
            ← Back to Medicine Catalog
          </button>
          <MedicineCard
            medicine={selectedMedicineData.data}
            aiAnalysis={selectedMedicineData.ai_explanation}
            source={selectedMedicineData.source}
            onCheckInteractions={onCheckInteractions}
          />
        </div>
      ) : (
        <div>
          {/* Category Filter Badges */}
          <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '12px', marginBottom: '24px' }}>
            <button
              className={`sample-pill ${activeCategory === 'All' ? 'active' : ''}`}
              style={activeCategory === 'All' ? { background: 'var(--primary)', color: '#fff' } : {}}
              onClick={() => setActiveCategory('All')}
            >
              All Categories
            </button>
            {categories.map((c, idx) => (
              <button
                key={idx}
                className={`sample-pill ${activeCategory === c.category ? 'active' : ''}`}
                style={activeCategory === c.category ? { background: 'var(--primary)', color: '#fff' } : {}}
                onClick={() => setActiveCategory(c.category)}
              >
                {c.category} ({c.count})
              </button>
            ))}
          </div>

          {/* Medicines Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
            {medicines
              .filter(m => activeCategory === 'All' || m.category === activeCategory)
              .map((med) => (
                <div 
                  key={med.id} 
                  className="glass-card glass-card-interactive" 
                  style={{ padding: '24px' }}
                  onClick={() => onSelectDrug(med.name)}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                    <h3 style={{ fontSize: '1.25rem' }}>{med.name}</h3>
                    <span className="badge badge-teal" style={{ fontSize: '0.7rem' }}>{med.category}</span>
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                    <strong>Generic:</strong> {med.generic_name}
                  </p>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '16px', lineHeight: 1.4 }}>
                    {med.common_uses.slice(0, 100)}...
                  </p>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', color: 'var(--primary)', fontWeight: 600 }}>
                    <span>View Monograph</span>
                    <ArrowRight size={16} />
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
