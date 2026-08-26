import React from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';

export default function DisclaimerBanner({ compact = false }) {
  if (compact) {
    return (
      <div style={{
        padding: '8px 14px',
        background: 'rgba(245, 158, 11, 0.1)',
        border: '1px solid rgba(245, 158, 11, 0.25)',
        borderRadius: 'var(--radius-sm)',
        fontSize: '0.8rem',
        color: 'var(--text-secondary)',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        margin: '12px 0'
      }}>
        <AlertTriangle size={16} color="var(--accent-amber)" />
        <span><strong>Educational Only:</strong> Not a medical diagnosis or prescription. Consult a healthcare provider.</span>
      </div>
    );
  }

  return (
    <div className="safety-banner" role="alert">
      <AlertTriangle className="safety-banner-icon" size={24} />
      <div className="safety-banner-content">
        <h4>Important Medical Safety Notice & Disclaimer</h4>
        <p>
          This application is an educational AI demonstration. It does 
          <strong> NOT</strong> diagnose medical conditions, provide personalized medical advice, or prescribe drugs. 
          Information is grounded in OpenFDA & verified pharmaceutical references. Always consult a qualified 
          doctor or pharmacist before taking or modifying any medication.
        </p>
      </div>
    </div>
  );
}
