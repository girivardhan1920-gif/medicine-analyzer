import React, { useState } from 'react';
import { 
  Pill, 
  AlertCircle, 
  ShieldAlert, 
  Sparkles, 
  Volume2, 
  VolumeX, 
  Check, 
  Copy, 
  Share2, 
  Building2, 
  Layers, 
  Bookmark, 
  ArrowRight,
  Archive
} from 'lucide-react';

export default function MedicineCard({ 
  medicine, 
  aiAnalysis, 
  source, 
  onCheckInteractions 
}) {
  const [speaking, setSpeaking] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!medicine) return null;

  // Text to speech reader
  const handleSpeak = () => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported on this browser.');
      return;
    }

    if (speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }

    const textToRead = `Medicine: ${medicine.name}. Generic name: ${medicine.generic_name}. Category: ${medicine.category}. Primary uses: ${medicine.common_uses}. Precautions: ${medicine.general_precautions}. Common side effects: ${medicine.common_side_effects}.`;
    const utterance = new SpeechSynthesisUtterance(textToRead);
    utterance.rate = 0.95;
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);

    window.speechSynthesis.speak(utterance);
    setSpeaking(true);
  };

  // Copy full profile summary
  const handleCopy = () => {
    const summaryText = `[MedAnalyze AI Report]
Medicine: ${medicine.name} (${medicine.generic_name})
Category: ${medicine.category}
Uses: ${medicine.common_uses}
Precautions: ${medicine.general_precautions}
Side Effects: ${medicine.common_side_effects}
Warnings: ${medicine.warnings}
Storage: ${medicine.storage_info}
Disclaimer: Educational use only. Consult a doctor.`;

    navigator.clipboard.writeText(summaryText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-card medicine-profile-card">
      {/* Header */}
      <div className="medicine-header">
        <div className="medicine-title-group">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            <h2>{medicine.name}</h2>
            <span className="badge badge-teal">{medicine.category}</span>
            {medicine.prescription_required ? (
              <span className="badge badge-rx" title="Prescription Required">Rx Only</span>
            ) : (
              <span className="badge badge-otc" title="Over-the-Counter">OTC</span>
            )}
          </div>
          <p className="medicine-generic-tag">
            <strong>Active Ingredient (Generic):</strong> {medicine.generic_name}
          </p>
          {medicine.brand_names && (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              <strong>Popular Brands:</strong> {medicine.brand_names}
            </p>
          )}
        </div>

        {/* Action Controls */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          <button 
            className="btn btn-secondary btn-sm" 
            onClick={handleSpeak}
            title={speaking ? 'Stop reading' : 'Read medical details aloud'}
          >
            {speaking ? <VolumeX size={16} color="var(--accent-rose)" /> : <Volume2 size={16} />}
            <span>{speaking ? 'Stop' : 'Listen'}</span>
          </button>

          <button 
            className="btn btn-secondary btn-sm" 
            onClick={handleCopy}
            title="Copy medicine summary"
          >
            {copied ? <Check size={16} color="var(--accent-emerald)" /> : <Copy size={16} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          {onCheckInteractions && (
            <button 
              className="btn btn-primary btn-sm"
              onClick={() => onCheckInteractions(medicine.name)}
            >
              <span>Check Interactions</span>
              <ArrowRight size={14} />
            </button>
          )}
        </div>
      </div>

      {/* AI Layman Explanation Banner */}
      {aiAnalysis && (
        <div className="ai-summary-highlight">
          <div className="ai-summary-header">
            <Sparkles size={20} />
            <span>AI Plain-Language Explanation</span>
          </div>
          <p style={{ fontSize: '0.95rem', color: 'var(--text-primary)', marginBottom: '12px' }}>
            {aiAnalysis.summary}
          </p>

          {aiAnalysis.key_takeaways && aiAnalysis.key_takeaways.length > 0 && (
            <div style={{ paddingLeft: '18px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
              <ul style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                {aiAnalysis.key_takeaways.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          <div style={{ marginTop: '12px', fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap' }}>
            <span>Grounding: {aiAnalysis.grounded_on || 'Verified Medical DB & OpenFDA'}</span>
            <span>Verified Source: {source || 'Local Verified Clinical Database'}</span>
          </div>
        </div>
      )}

      {/* Detailed Clinical Info Grid */}
      <div className="medicine-info-grid">
        {/* 1. Common Uses */}
        <div className="info-box">
          <div className="info-box-title">
            <Pill size={16} color="var(--primary)" />
            <span>Common Medical Uses</span>
          </div>
          <p className="info-box-content">{medicine.common_uses}</p>
        </div>

        {/* 2. Precautions */}
        <div className="info-box caution-box">
          <div className="info-box-title">
            <AlertCircle size={16} />
            <span>General Precautions</span>
          </div>
          <p className="info-box-content">{medicine.general_precautions}</p>
        </div>

        {/* 3. Side Effects */}
        <div className="info-box">
          <div className="info-box-title">
            <Layers size={16} color="var(--accent-purple)" />
            <span>Common Side Effects</span>
          </div>
          <p className="info-box-content">{medicine.common_side_effects}</p>
        </div>

        {/* 4. Boxed Warnings */}
        <div className="info-box warning-box">
          <div className="info-box-title">
            <ShieldAlert size={16} />
            <span>Clinical Warnings & Hazards</span>
          </div>
          <p className="info-box-content">{medicine.warnings}</p>
        </div>

        {/* 5. Storage Info */}
        <div className="info-box">
          <div className="info-box-title">
            <Archive size={16} color="var(--accent-teal)" />
            <span>Storage & Handling</span>
          </div>
          <p className="info-box-content">{medicine.storage_info}</p>
        </div>

        {/* 6. Manufacturing & Dosage Forms */}
        <div className="info-box">
          <div className="info-box-title">
            <Building2 size={16} color="var(--text-muted)" />
            <span>Forms & Manufacturer</span>
          </div>
          <p className="info-box-content">
            <strong>Available Forms:</strong> {medicine.dosage_forms || 'Tablet / Capsule'}<br />
            <strong>Primary Manufacturer:</strong> {medicine.manufacturer || 'Approved Pharmaceutical Mfr'}
          </p>
        </div>
      </div>
    </div>
  );
}
