import React from 'react';
import { 
  ShieldCheck, 
  Cpu, 
  Database, 
  Layers, 
  AlertOctagon, 
  CheckCircle, 
  GraduationCap, 
  Code,
  Lock,
  ExternalLink
} from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';

export default function AboutPage() {
  return (
    <div style={{ maxWidth: '960px', margin: '0 auto' }}>
      <DisclaimerBanner />

      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <div className="hero-tag">
          <GraduationCap size={16} />
          <span>Medical Intelligence & Architecture Hub</span>
        </div>
        <h2 style={{ fontSize: '2.2rem', marginBottom: '8px' }}>
          AI Medicine Analyzer System Architecture
        </h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '700px', margin: '0 auto' }}>
          An educational healthcare intelligence platform designed to eliminate pharmaceutical ambiguity, 
          prevent adverse drug interactions, and translate clinical jargon for everyday patients.
        </p>
      </div>

      {/* System Flow Grid */}
      <div className="glass-card" style={{ padding: '28px', marginBottom: '28px' }}>
        <h3 style={{ fontSize: '1.25rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Layers size={20} color="var(--primary)" />
          <span>End-to-End Analysis Workflow</span>
        </h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', textAlign: 'center' }}>
          <div style={{ background: 'var(--bg-surface)', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--primary)', marginBottom: '4px' }}>Step 1</div>
            <h4 style={{ fontSize: '0.95rem', marginBottom: '6px' }}>Input / OCR Scan</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>User enters medicine name or uploads package photo.</p>
          </div>

          <div style={{ background: 'var(--bg-surface)', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--primary)', marginBottom: '4px' }}>Step 2</div>
            <h4 style={{ fontSize: '0.95rem', marginBottom: '6px' }}>OCR & Token Match</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Image filtered via PIL/OCR and matched with known compounds.</p>
          </div>

          <div style={{ background: 'var(--bg-surface)', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--primary)', marginBottom: '4px' }}>Step 3</div>
            <h4 style={{ fontSize: '0.95rem', marginBottom: '6px' }}>Database & FDA Sync</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Ground truth verified against SQLite DB & live OpenFDA API.</p>
          </div>

          <div style={{ background: 'var(--bg-surface)', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--primary)', marginBottom: '4px' }}>Step 4</div>
            <h4 style={{ fontSize: '0.95rem', marginBottom: '6px' }}>AI Simplification</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>AI summarizes facts in simple language with safety flags.</p>
          </div>
        </div>
      </div>

      {/* Safety Guardrails Card */}
      <div className="glass-card" style={{ padding: '28px', marginBottom: '28px', borderLeft: '4px solid var(--accent-amber)' }}>
        <h3 style={{ fontSize: '1.25rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-amber)' }}>
          <ShieldCheck size={22} />
          <span>Strict AI Medical Guardrails & Ethics Policy</span>
        </h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle size={18} color="var(--accent-emerald)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              <strong>Zero Hallucination Grounding:</strong> Facts are anchored in verified pharmaceutical databases. The AI is prevented from fabricating facts.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle size={18} color="var(--accent-emerald)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              <strong>No Diagnosis or Prescription:</strong> The system strictly rejects requests to diagnose diseases, prescribe dosages, or alter physician treatments.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle size={18} color="var(--accent-emerald)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              <strong>Emergency Triaging:</strong> Critical keywords (overdose, chest pain, difficulty breathing) trigger instant emergency escalation warnings.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle size={18} color="var(--accent-emerald)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              <strong>Universal Medical Disclaimers:</strong> Every query response and page prominently reminds users that this platform is educational only.
            </p>
          </div>
        </div>
      </div>

      {/* Tech Stack Rundown */}
      <div className="glass-card" style={{ padding: '28px', marginBottom: '28px' }}>
        <h3 style={{ fontSize: '1.25rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Code size={20} color="var(--primary)" />
          <span>Technology Stack Specifications</span>
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px' }}>
          <div>
            <h4 style={{ fontSize: '1rem', color: 'var(--primary)', marginBottom: '8px' }}>Frontend Layer</h4>
            <ul style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', paddingLeft: '18px', lineHeight: 1.6 }}>
              <li><strong>Framework:</strong> React 18 (Vite Bundler)</li>
              <li><strong>Styling:</strong> Custom Glassmorphic CSS with CSS Variables</li>
              <li><strong>Icons:</strong> Lucide-React SVG Library</li>
              <li><strong>Accessibility:</strong> Web Speech API Audio Synthesizer</li>
            </ul>
          </div>

          <div>
            <h4 style={{ fontSize: '1rem', color: 'var(--accent-teal)', marginBottom: '8px' }}>Backend Layer</h4>
            <ul style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', paddingLeft: '18px', lineHeight: 1.6 }}>
              <li><strong>Server:</strong> Python 3.14 + Flask REST APIs</li>
              <li><strong>Database:</strong> SQLite 3 (Upgrade-ready for PostgreSQL)</li>
              <li><strong>CORS:</strong> Flask-CORS Middleware</li>
              <li><strong>External API:</strong> Official OpenFDA Drug Label API</li>
            </ul>
          </div>

          <div>
            <h4 style={{ fontSize: '1rem', color: 'var(--accent-purple)', marginBottom: '8px' }}>AI & Computer Vision</h4>
            <ul style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', paddingLeft: '18px', lineHeight: 1.6 }}>
              <li><strong>Vision / OCR:</strong> Pillow Pre-Processing + Pytesseract / Gemini Vision</li>
              <li><strong>LLM Engine:</strong> Google Gemini 1.5 Flash + Deterministic Clinical Grounding Engine</li>
              <li><strong>Interaction Engine:</strong> Multi-pair matrix evaluation algorithm</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Technical Q&A Cheat Sheet */}
      <div className="glass-card" style={{ padding: '28px' }}>
        <h3 style={{ fontSize: '1.25rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <GraduationCap size={20} color="var(--accent-rose)" />
          <span>Technical Architecture & Safety Q&A</span>
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', fontSize: '0.9rem' }}>
          <div style={{ background: 'var(--bg-surface)', padding: '14px 18px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <strong>Q1: How does the system prevent medical AI hallucinations?</strong>
            <p style={{ color: 'var(--text-secondary)', marginTop: '4px', fontSize: '0.85rem' }}>
              The backend queries authoritative medical databases (OpenFDA and local SQLite clinical compendium) first. 
              The AI model is constrained strictly to synthesize only the verified retrieved pharmacological data.
            </p>
          </div>

          <div style={{ background: 'var(--bg-surface)', padding: '14px 18px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <strong>Q2: How are multi-drug interactions evaluated?</strong>
            <p style={{ color: 'var(--text-secondary)', marginTop: '4px', fontSize: '0.85rem' }}>
              The system calculates pairwise combinations across all submitted drugs, searches symmetrical relationship rules in the interaction matrix, 
              and ranks findings by Major, Moderate, or Minor clinical severity.
            </p>
          </div>

          <div style={{ background: 'var(--bg-surface)', padding: '14px 18px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <strong>Q3: How does the OCR pipeline extract text from medicine packaging?</strong>
            <p style={{ color: 'var(--text-secondary)', marginTop: '4px', fontSize: '0.85rem' }}>
              Uploaded images are enhanced via contrast stretching, grayscale conversion, and edge sharpening using PIL, 
              followed by OCR tokenization and fuzzy keyword matching against international generic and brand name registries.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
