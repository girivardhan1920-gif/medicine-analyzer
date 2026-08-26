import React from 'react';
import { Bot, User, AlertOctagon, CheckCircle } from 'lucide-react';

export default function ChatMessage({ message }) {
  const isUser = message.sender === 'user';
  const isEmergency = message.safety_flag === 1;

  // Format bold and bullet points in text
  const formatText = (text) => {
    if (!text) return '';
    return text.split('\n').map((line, idx) => {
      // Replace **text** with <strong>text</strong>
      const parts = line.split(/(\*\*.*?\*\*)/g);
      return (
        <span key={idx} style={{ display: 'block', minHeight: line === '' ? '8px' : 'auto' }}>
          {parts.map((p, pIdx) => {
            if (p.startsWith('**') && p.endsWith('**')) {
              return <strong key={pIdx}>{p.slice(2, -2)}</strong>;
            }
            return p;
          })}
        </span>
      );
    });
  };

  return (
    <div style={{
      display: 'flex',
      gap: '12px',
      alignItems: 'flex-start',
      justifyContent: isUser ? 'flex-end' : 'flex-start'
    }}>
      {!isUser && (
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: 'var(--radius-full)',
          background: isEmergency ? 'rgba(225, 29, 72, 0.15)' : 'var(--primary-light)',
          color: isEmergency ? 'var(--accent-rose)' : 'var(--primary)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0
        }}>
          {isEmergency ? <AlertOctagon size={20} /> : <Bot size={20} />}
        </div>
      )}

      <div className={`chat-bubble ${isUser ? 'user' : 'ai'} ${isEmergency ? 'emergency' : ''}`}>
        {message.matched_drug && (
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '4px',
            padding: '2px 8px',
            borderRadius: 'var(--radius-full)',
            background: 'var(--primary-light)',
            color: 'var(--primary)',
            fontSize: '0.75rem',
            fontWeight: 700,
            marginBottom: '8px'
          }}>
            <CheckCircle size={12} />
            <span>Grounded on: {message.matched_drug}</span>
          </div>
        )}

        <div style={{ whiteSpace: 'pre-wrap' }}>
          {formatText(message.text)}
        </div>

        <div style={{
          fontSize: '0.7rem',
          color: isUser ? 'rgba(255, 255, 255, 0.7)' : 'var(--text-muted)',
          marginTop: '6px',
          textAlign: isUser ? 'right' : 'left'
        }}>
          {message.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>

      {isUser && (
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: 'var(--radius-full)',
          background: 'var(--bg-elevated)',
          color: 'var(--text-primary)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0
        }}>
          <User size={20} />
        </div>
      )}
    </div>
  );
}
