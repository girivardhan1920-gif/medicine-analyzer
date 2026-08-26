import React, { useState, useEffect, useRef } from 'react';
import { Bot, Send, Sparkles, RefreshCw, HelpCircle, ShieldAlert, AlertCircle } from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';
import ChatMessage from '../components/ChatMessage';
import { sendChatMessage, getSamplePrompts } from '../services/api';

export default function AssistantPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: "Hello! I am your **AI Pharmacist Assistant**. I can help explain medicine purposes, generic names, common side effects, storage guidelines, and potential drug interactions.\n\n*Note: I cannot diagnose conditions or prescribe treatments. Always consult a healthcare provider for medical decisions.*",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [samplePrompts, setSamplePrompts] = useState([]);
  const chatEndRef = useRef(null);

  useEffect(() => {
    getSamplePrompts().then(res => res.prompts && setSamplePrompts(res.prompts)).catch(console.error);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (textToSend) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || loading) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: text.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const res = await sendChatMessage(text.trim());
      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: res.reply,
        safety_flag: res.safety_flag,
        matched_drug: res.matched_drug,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      const errorMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: 'Sorry, I encountered an error connecting to the medical AI service. Please try again.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '880px', margin: '0 auto' }}>
      <DisclaimerBanner compact />

      <div className="glass-card chat-container">
        {/* Chat Header */}
        <div style={{
          padding: '16px 24px',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '38px',
              height: '38px',
              borderRadius: 'var(--radius-md)',
              background: 'linear-gradient(135deg, #0ea5e9, #0d9488)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff'
            }}>
              <Bot size={22} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.1rem' }}>AI Clinical Knowledge Assistant</h3>
              <p style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-emerald)', display: 'inline-block' }}></span>
                Grounded on OpenFDA & Verified Medical Records
              </p>
            </div>
          </div>

          <button 
            className="btn btn-secondary btn-sm"
            onClick={() => setMessages([messages[0]])}
            title="Reset conversation"
          >
            Clear Chat
          </button>
        </div>

        {/* Chat Message Feed */}
        <div className="chat-box">
          {messages.map((m) => (
            <ChatMessage key={m.id} message={m} />
          ))}

          {loading && (
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: 'var(--radius-full)',
                background: 'var(--primary-light)',
                color: 'var(--primary)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Bot size={20} />
              </div>
              <div className="chat-bubble ai" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <RefreshCw className="spin-icon" size={16} color="var(--primary)" />
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  Consulting verified medical compendium & synthesizing explanation...
                </span>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Quick starter suggestion chips */}
        {samplePrompts.length > 0 && messages.length <= 2 && (
          <div style={{ padding: '8px 20px', display: 'flex', gap: '6px', overflowX: 'auto', borderTop: '1px solid var(--border-subtle)' }}>
            {samplePrompts.slice(0, 3).map((prompt, idx) => (
              <button
                key={idx}
                className="sample-pill"
                style={{ fontSize: '0.75rem', whiteSpace: 'nowrap' }}
                onClick={() => handleSendMessage(prompt)}
              >
                {prompt}
              </button>
            ))}
          </div>
        )}

        {/* Chat Input Bar */}
        <div className="chat-input-bar">
          <input
            id="chat-user-input"
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask a medical question (e.g. 'What are the warnings for Omeprazole?')..."
            disabled={loading}
          />
          <button
            id="chat-send-btn"
            className="btn btn-primary"
            onClick={() => handleSendMessage()}
            disabled={loading || !inputMessage.trim()}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
