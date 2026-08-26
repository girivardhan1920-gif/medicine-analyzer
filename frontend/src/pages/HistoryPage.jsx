import React, { useState, useEffect } from 'react';
import { History, Filter, Trash2, RefreshCw } from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';
import HistoryTable from '../components/HistoryTable';
import { getSearchHistory, deleteHistoryItem, clearSearchHistory } from '../services/api';

export default function HistoryPage({ onSelectQuery }) {
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({});
  const [filterType, setFilterType] = useState('');
  const [loading, setLoading] = useState(false);

  const loadHistory = (type = filterType) => {
    setLoading(true);
    getSearchHistory(type)
      .then(res => {
        setHistory(res.history || []);
        setStats(res.stats || {});
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadHistory();
  }, [filterType]);

  const handleDelete = async (id) => {
    try {
      await deleteHistoryItem(id);
      setHistory(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const handleClear = async () => {
    if (window.confirm('Are you sure you want to clear all analysis history?')) {
      try {
        await clearSearchHistory();
        setHistory([]);
      } catch (err) {
        console.error(err);
      }
    }
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <DisclaimerBanner />

      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '6px' }}>Search & Analysis History</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Review past medicine searches, OCR image extractions, and drug interaction audits.
        </p>
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            className={`sample-pill ${filterType === '' ? 'active' : ''}`}
            style={filterType === '' ? { background: 'var(--primary)', color: '#fff' } : {}}
            onClick={() => setFilterType('')}
          >
            All Logs ({stats.total_searches || history.length})
          </button>
          <button
            className={`sample-pill ${filterType === 'text' ? 'active' : ''}`}
            style={filterType === 'text' ? { background: 'var(--primary)', color: '#fff' } : {}}
            onClick={() => setFilterType('text')}
          >
            Text Searches ({stats.text_searches || 0})
          </button>
          <button
            className={`sample-pill ${filterType === 'image_ocr' ? 'active' : ''}`}
            style={filterType === 'image_ocr' ? { background: 'var(--primary)', color: '#fff' } : {}}
            onClick={() => setFilterType('image_ocr')}
          >
            Image OCR ({stats.image_searches || 0})
          </button>
          <button
            className={`sample-pill ${filterType === 'interaction' ? 'active' : ''}`}
            style={filterType === 'interaction' ? { background: 'var(--primary)', color: '#fff' } : {}}
            onClick={() => setFilterType('interaction')}
          >
            Interactions ({stats.interaction_checks || 0})
          </button>
        </div>

        <button 
          className="btn btn-secondary btn-sm" 
          onClick={() => loadHistory()}
          disabled={loading}
        >
          <RefreshCw className={loading ? 'spin-icon' : ''} size={14} />
          <span>Refresh</span>
        </button>
      </div>

      {/* History Table */}
      <HistoryTable
        history={history}
        onDelete={handleDelete}
        onClear={handleClear}
        onSelectQuery={onSelectQuery}
      />
    </div>
  );
}
