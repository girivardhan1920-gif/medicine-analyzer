import React from 'react';
import { Search, Image as ImageIcon, Pill, Trash2, ArrowRight, Download, RefreshCw } from 'lucide-react';

export default function HistoryTable({ 
  history = [], 
  onDelete, 
  onClear, 
  onSelectQuery 
}) {
  const exportToCSV = () => {
    if (!history.length) return;
    const headers = ['ID', 'Query', 'Type', 'Summary', 'Matched Medicine', 'Timestamp'];
    const rows = history.map(h => [
      h.id,
      `"${(h.query || '').replace(/"/g, '""')}"`,
      h.search_type,
      `"${(h.result_summary || '').replace(/"/g, '""')}"`,
      `"${(h.matched_medicine || '').replace(/"/g, '""')}"`,
      h.created_at
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `medicine_analyzer_history_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getTypeBadge = (type) => {
    switch (type) {
      case 'image_ocr':
        return (
          <span className="badge badge-teal">
            <ImageIcon size={12} /> Image OCR
          </span>
        );
      case 'interaction':
        return (
          <span className="badge badge-major">
            <Pill size={12} /> Interaction
          </span>
        );
      default:
        return (
          <span className="badge badge-primary">
            <Search size={12} /> Text Search
          </span>
        );
    }
  };

  return (
    <div className="glass-card" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '20px' }}>
        <div>
          <h3 style={{ fontSize: '1.25rem' }}>Recent Analysis Ledger</h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Audit log of all medicines, OCR scans, and multi-drug interaction queries.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button 
            className="btn btn-secondary btn-sm" 
            onClick={exportToCSV}
            disabled={!history.length}
            title="Download search logs as CSV"
          >
            <Download size={15} />
            <span>Export CSV</span>
          </button>

          <button 
            className="btn btn-danger btn-sm" 
            onClick={onClear}
            disabled={!history.length}
            title="Clear all recorded history"
          >
            <Trash2 size={15} />
            <span>Clear History</span>
          </button>
        </div>
      </div>

      {history.length > 0 ? (
        <div className="history-table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Search Query</th>
                <th>Result Summary</th>
                <th>Date & Time</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id}>
                  <td>{getTypeBadge(item.search_type)}</td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                    {item.query}
                  </td>
                  <td>{item.result_summary || 'Analysis Completed'}</td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    {new Date(item.created_at).toLocaleString([], {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <div style={{ display: 'inline-flex', gap: '6px' }}>
                      {item.matched_medicine && onSelectQuery && (
                        <button
                          className="btn btn-secondary btn-sm"
                          style={{ padding: '4px 8px' }}
                          onClick={() => onSelectQuery(item.matched_medicine, item.search_type)}
                          title="Re-analyze this medicine"
                        >
                          <ArrowRight size={14} />
                        </button>
                      )}
                      <button
                        className="btn btn-secondary btn-sm"
                        style={{ padding: '4px 8px', color: 'var(--accent-rose)' }}
                        onClick={() => onDelete(item.id)}
                        title="Delete log entry"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)' }}>
          <p>No search history recorded yet. Start by searching or uploading a medicine package!</p>
        </div>
      )}
    </div>
  );
}
