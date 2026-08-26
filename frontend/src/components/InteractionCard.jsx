import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle2, UserCheck, Stethoscope } from 'lucide-react';

export default function InteractionCard({ result }) {
  if (!result) return null;

  const {
    drugs_checked = [],
    total_interactions = 0,
    major_count = 0,
    moderate_count = 0,
    minor_count = 0,
    risk_level = 'None Detected',
    consultation_recommended = false,
    consultation_message = '',
    interactions = []
  } = result;

  const isMajor = major_count > 0;
  const isModerate = !isMajor && moderate_count > 0;
  const isSafe = total_interactions === 0;

  let gaugeClass = 'minor';
  if (isMajor) gaugeClass = 'major';
  else if (isModerate) gaugeClass = 'moderate';

  return (
    <div className="glass-card interaction-result-card">
      {/* Top Severity Banner */}
      <div className={`severity-gauge ${gaugeClass}`}>
        {isMajor ? (
          <ShieldAlert size={36} color="var(--accent-rose)" />
        ) : isModerate ? (
          <AlertTriangle size={36} color="var(--accent-amber)" />
        ) : (
          <CheckCircle2 size={36} color="var(--accent-emerald)" />
        )}
        <div>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginBottom: '2px' }}>
            {risk_level}
          </h3>
          <p style={{ fontSize: '0.85rem' }}>
            Evaluated {drugs_checked.length} medicines: {drugs_checked.join(', ')}
          </p>
        </div>
      </div>

      {/* Doctor Consultation Callout */}
      {consultation_recommended && (
        <div style={{
          padding: '16px 20px',
          background: isMajor ? 'rgba(225, 29, 72, 0.08)' : 'rgba(217, 119, 6, 0.08)',
          border: `1px solid ${isMajor ? 'rgba(225, 29, 72, 0.3)' : 'rgba(217, 119, 6, 0.3)'}`,
          borderRadius: 'var(--radius-md)',
          display: 'flex',
          alignItems: 'center',
          gap: '14px',
          marginBottom: '24px'
        }}>
          <Stethoscope size={28} color={isMajor ? 'var(--accent-rose)' : 'var(--accent-amber)'} />
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: isMajor ? 'var(--accent-rose)' : 'var(--accent-amber)', marginBottom: '2px' }}>
              Action Required: Professional Consultation Advised
            </h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              {consultation_message}
            </p>
          </div>
        </div>
      )}

      {/* Interactions List */}
      {interactions.length > 0 ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h4 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
            Identified Interaction Pairs ({interactions.length})
          </h4>

          {interactions.map((item, idx) => (
            <div 
              key={idx} 
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '20px',
                borderLeft: `4px solid ${
                  item.severity === 'Major' ? 'var(--accent-rose)' :
                  item.severity === 'Moderate' ? 'var(--accent-amber)' : 'var(--accent-emerald)'
                }`
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <h5 style={{ fontSize: '1.05rem', fontWeight: 700 }}>
                  {item.drug_a} ↔ {item.drug_b}
                </h5>
                <span className={`badge ${
                  item.severity === 'Major' ? 'badge-major' :
                  item.severity === 'Moderate' ? 'badge-moderate' : 'badge-minor'
                }`}>
                  {item.severity} Severity
                </span>
              </div>

              <p style={{ fontSize: '0.9rem', color: 'var(--text-primary)', marginBottom: '12px', lineHeight: 1.5 }}>
                <strong>Clinical Effect:</strong> {item.description}
              </p>

              <div style={{
                background: 'var(--bg-elevated)',
                padding: '10px 14px',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.85rem',
                color: 'var(--text-secondary)'
              }}>
                <strong>Clinical Management / Recommendation:</strong> {item.recommendation}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{
          padding: '30px',
          textAlign: 'center',
          background: 'var(--bg-surface)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)'
        }}>
          <CheckCircle2 size={40} color="var(--accent-emerald)" style={{ margin: '0 auto 12px' }} />
          <h4 style={{ fontSize: '1.1rem', marginBottom: '6px' }}>No High-Risk Interactions Found</h4>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', maxWidth: '500px', margin: '0 auto' }}>
            No dangerous drug-to-drug interactions were detected in our verified clinical database between 
            <strong> {drugs_checked.join(' and ')}</strong>. Always inform your prescribing doctor of all medications you take.
          </p>
        </div>
      )}
    </div>
  );
}
