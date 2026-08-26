import React, { useState } from 'react';
import { 
  Search, 
  ScanLine, 
  UploadCloud, 
  RefreshCw, 
  AlertCircle, 
  CheckCircle, 
  FileText, 
  Sparkles,
  ArrowRight
} from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';
import MedicineCard from '../components/MedicineCard';
import ImageUploader from '../components/ImageUploader';
import { analyzeMedicine, analyzeMedicineImage, searchMedicines } from '../services/api';

export default function AnalyzerPage({ 
  initialMedicine = '', 
  onCheckInteractions 
}) {
  const [activeTab, setActiveTab] = useState('text'); // 'text' or 'image'
  const [searchQuery, setSearchQuery] = useState(initialMedicine || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [ocrDetails, setOcrDetails] = useState(null);

  // Auto-analyze if initialMedicine prop was passed
  React.useEffect(() => {
    if (initialMedicine && initialMedicine.trim()) {
      handleTextAnalyze(initialMedicine.trim());
    }
  }, [initialMedicine]);

  const handleTextAnalyze = async (drugName) => {
    const target = drugName || searchQuery;
    if (!target.trim()) return;

    setLoading(true);
    setError(null);
    setOcrDetails(null);

    try {
      const res = await analyzeMedicine(target.trim());
      setAnalysisResult(res);
    } catch (err) {
      setError(err.message || `No verified information found for '${target}'.`);
      setAnalysisResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleImageAnalyze = async (imageFile) => {
    setLoading(true);
    setError(null);
    setAnalysisResult(null);
    setOcrDetails(null);

    try {
      const res = await analyzeMedicineImage(imageFile);
      setOcrDetails(res.ocr_details);
      if (res.matched && res.medicine) {
        setAnalysisResult({
          source: res.ocr_details.method,
          medicine: res.medicine,
          ai_analysis: res.ai_analysis,
          disclaimer: res.disclaimer
        });
      } else {
        setError(`OCR extracted text, but could not match a verified drug in the clinical database.`);
      }
    } catch (err) {
      setError(err.message || 'Image processing failed. Please try another image.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analyzer-container">
      <DisclaimerBanner />

      <div style={{ textAlign: 'center', marginBottom: '28px' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '6px' }}>Medicine Analyzer</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Enter a medicine name or upload package photos to identify ingredients, uses, and side effects.
        </p>
      </div>

      {/* Analyzer Mode Selector Tabs */}
      <div className="tabs-nav" style={{ justifyContent: 'center' }}>
        <button
          id="analyzer-tab-text"
          className={`tab-btn ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => { setActiveTab('text'); setError(null); }}
        >
          <Search size={18} />
          <span>Search by Name</span>
        </button>

        <button
          id="analyzer-tab-image"
          className={`tab-btn ${activeTab === 'image' ? 'active' : ''}`}
          onClick={() => { setActiveTab('image'); setError(null); }}
        >
          <ScanLine size={18} />
          <span>Upload Package Image (OCR)</span>
        </button>
      </div>

      {/* Tab 1: Text Search Input */}
      {activeTab === 'text' && (
        <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
          <form onSubmit={(e) => { e.preventDefault(); handleTextAnalyze(); }}>
            <div style={{ display: 'flex', gap: '12px' }}>
              <div className="search-input-box" style={{ flex: 1 }}>
                <Search size={20} color="var(--primary)" style={{ marginRight: '10px' }} />
                <input
                  id="analyzer-search-input"
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Enter brand name or generic compound (e.g. Paracetamol, Lisinopril, Azithromycin)..."
                />
              </div>
              <button 
                id="analyzer-submit-btn"
                type="submit" 
                className="btn btn-primary" 
                disabled={loading || !searchQuery.trim()}
              >
                {loading ? <RefreshCw className="spin-icon" size={18} /> : <Sparkles size={18} />}
                <span>Analyze</span>
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Tab 2: Image OCR Uploader */}
      {activeTab === 'image' && (
        <div style={{ marginBottom: '24px' }}>
          <ImageUploader onAnalyzeImage={handleImageAnalyze} loading={loading} />
        </div>
      )}

      {/* OCR Recognition Feedback Card */}
      {ocrDetails && (
        <div className="glass-card" style={{ padding: '20px', marginBottom: '20px', borderLeft: '4px solid var(--primary)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <h4 style={{ fontSize: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ScanLine size={18} color="var(--primary)" />
              OCR Detection Results
            </h4>
            <span className="badge badge-teal">
              Confidence: {Math.round((ocrDetails.confidence || 0.9) * 100)}%
            </span>
          </div>
          <p style={{ fontSize: '0.9rem', marginBottom: '4px' }}>
            <strong>Recognized Drug:</strong> {ocrDetails.detected_name}
          </p>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            <strong>Engine:</strong> {ocrDetails.method} | <strong>Raw OCR Text:</strong> "{ocrDetails.raw_ocr_text}"
          </p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div style={{
          padding: '16px 20px',
          background: 'rgba(225, 29, 72, 0.08)',
          border: '1px solid rgba(225, 29, 72, 0.3)',
          borderRadius: 'var(--radius-md)',
          color: 'var(--accent-rose)',
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          marginBottom: '24px'
        }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Analysis Results View */}
      {analysisResult && analysisResult.medicine && (
        <MedicineCard
          medicine={analysisResult.medicine}
          aiAnalysis={analysisResult.ai_analysis}
          source={analysisResult.source}
          onCheckInteractions={onCheckInteractions}
        />
      )}
    </div>
  );
}
