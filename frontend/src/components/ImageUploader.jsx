import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, Camera, RefreshCw, CheckCircle, AlertCircle, FileText } from 'lucide-react';

export default function ImageUploader({ onAnalyzeImage, loading }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  // Sample medicine packages for one-click demonstration
  const samplePresets = [
    { label: 'Paracetamol 650mg Package', name: 'Paracetamol_650mg_Strip.jpg', mockDrug: 'Paracetamol' },
    { label: 'Amoxicillin 500mg Box', name: 'Amoxicillin_500mg_Antibiotic.jpg', mockDrug: 'Amoxicillin' },
    { label: 'Metformin 500mg Tablet', name: 'Metformin_Glucophage_500mg.jpg', mockDrug: 'Metformin' },
    { label: 'Atorvastatin 20mg Pack', name: 'Atorvastatin_Lipitor_20mg.jpg', mockDrug: 'Atorvastatin' },
  ];

  const handleFileChange = (file) => {
    if (!file) return;
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handlePresetSelect = (preset) => {
    // Generate a mock canvas image with the drug name printed for clean OCR testing
    const canvas = document.createElement('canvas');
    canvas.width = 600;
    canvas.height = 350;
    const ctx = canvas.getContext('2d');

    // Draw background
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, 600, 350);

    // Draw medical banner
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(0, 0, 600, 70);

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 26px sans-serif';
    ctx.fillText('PHARMACEUTICAL PACKAGING', 40, 46);

    // Draw drug name
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 44px sans-serif';
    ctx.fillText(preset.mockDrug.toUpperCase(), 40, 150);

    // Draw dosage
    ctx.fillStyle = '#475569';
    ctx.font = '22px sans-serif';
    ctx.fillText('500 mg Film-Coated Tablets', 40, 200);
    ctx.fillText('Rx Only - Keep out of reach of children', 40, 240);
    ctx.fillText('Batch No: EXP-2027 | Mfr: MedTech Labs', 40, 280);

    canvas.toBlob((blob) => {
      const file = new File([blob], preset.name, { type: 'image/jpeg' });
      handleFileChange(file);
    }, 'image/jpeg');
  };

  const handleSubmit = () => {
    if (!selectedFile) return;
    onAnalyzeImage(selectedFile);
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="glass-card" style={{ padding: '30px' }}>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/png, image/jpeg, image/jpg, image/webp"
        style={{ display: 'none' }}
        onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
      />

      {/* Dropzone or Preview */}
      {!previewUrl ? (
        <div
          className={`dropzone ${dragActive ? 'dragover' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="dropzone-icon">
            <UploadCloud size={32} />
          </div>
          <h3 style={{ fontSize: '1.2rem', marginBottom: '8px' }}>
            Upload Medicine Package or Prescription Photo
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '16px' }}>
            Drag & drop an image here, or click to browse (PNG, JPG, WEBP up to 16MB)
          </p>
          <button type="button" className="btn btn-secondary btn-sm" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
            <ImageIcon size={16} />
            <span>Select Image File</span>
          </button>
        </div>
      ) : (
        <div style={{ textAlign: 'center' }}>
          <div style={{
            maxWidth: '450px',
            margin: '0 auto 20px',
            border: '2px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            overflow: 'hidden',
            background: '#000',
            maxHeight: '300px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <img 
              src={previewUrl} 
              alt="Uploaded medicine preview" 
              style={{ maxWidth: '100%', maxHeight: '290px', objectFit: 'contain' }} 
            />
          </div>

          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
            Selected: <strong>{selectedFile?.name}</strong> ({(selectedFile?.size / 1024).toFixed(1)} KB)
          </p>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '12px' }}>
            <button 
              className="btn btn-primary"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? (
                <>
                  <RefreshCw className="spin-icon" size={18} />
                  <span>Processing OCR & AI...</span>
                </>
              ) : (
                <>
                  <CheckCircle size={18} />
                  <span>Analyze Medicine Image</span>
                </>
              )}
            </button>

            <button 
              className="btn btn-secondary"
              onClick={handleReset}
              disabled={loading}
            >
              <RefreshCw size={16} />
              <span>Choose Another</span>
            </button>
          </div>
        </div>
      )}

      {/* Preset sample packages for demonstration */}
      <div className="sample-prescriptions-bar">
        <h4>Instant Demo Packages (Click to Test OCR):</h4>
        <div className="sample-pills">
          {samplePresets.map((p, idx) => (
            <button
              key={idx}
              type="button"
              className="sample-pill"
              onClick={() => handlePresetSelect(p)}
            >
              <FileText size={14} style={{ marginRight: '4px', verticalAlign: 'middle' }} />
              {p.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
