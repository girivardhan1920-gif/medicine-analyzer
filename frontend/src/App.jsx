import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import AnalyzerPage from './pages/AnalyzerPage';
import DetailsPage from './pages/DetailsPage';
import InteractionPage from './pages/InteractionPage';
import AssistantPage from './pages/AssistantPage';
import HistoryPage from './pages/HistoryPage';
import AboutPage from './pages/AboutPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [selectedDrug, setSelectedDrug] = useState('');
  const [interactionMeds, setInteractionMeds] = useState([]);
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('med_theme') || 'dark';
  });

  // Apply theme to document root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('med_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  // Quick navigation handlers
  const handleSelectMedicineFromHome = (medicineName) => {
    setSelectedDrug(medicineName);
    setActiveTab('analyzer');
  };

  const handleCheckInteractionsForDrug = (medicineName) => {
    setInteractionMeds([medicineName]);
    setActiveTab('interactions');
  };

  const handleSelectFromHistory = (matchedDrug, type) => {
    if (type === 'interaction') {
      const parts = matchedDrug.split(',').map(s => s.trim()).filter(Boolean);
      setInteractionMeds(parts.length ? parts : ['Aspirin', 'Warfarin']);
      setActiveTab('interactions');
    } else {
      setSelectedDrug(matchedDrug);
      setActiveTab('analyzer');
    }
  };

  return (
    <div className="app-container">
      {/* Top Navigation Bar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        theme={theme}
        toggleTheme={toggleTheme}
      />

      {/* Main Page Body */}
      <main className="main-content">
        {activeTab === 'home' && (
          <HomePage
            onNavigate={setActiveTab}
            onSelectMedicine={handleSelectMedicineFromHome}
          />
        )}

        {activeTab === 'analyzer' && (
          <AnalyzerPage
            initialMedicine={selectedDrug}
            onCheckInteractions={handleCheckInteractionsForDrug}
          />
        )}

        {activeTab === 'details' && (
          <DetailsPage
            selectedDrug={selectedDrug}
            onSelectDrug={(drug) => { setSelectedDrug(drug); setActiveTab('analyzer'); }}
            onCheckInteractions={handleCheckInteractionsForDrug}
          />
        )}

        {activeTab === 'interactions' && (
          <InteractionPage
            preSelectedMeds={interactionMeds}
          />
        )}

        {activeTab === 'assistant' && (
          <AssistantPage />
        )}

        {activeTab === 'history' && (
          <HistoryPage
            onSelectQuery={handleSelectFromHistory}
          />
        )}

        {activeTab === 'about' && (
          <AboutPage />
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <strong>MedAnalyze AI</strong> — Intelligent Pharmaceutical Analysis Platform
          </div>
          <div>
            Data Grounded via <a href="https://open.fda.gov" target="_blank" rel="noreferrer" style={{ color: 'var(--primary)', textDecoration: 'none' }}>OpenFDA</a> & Curated Pharmacopeia
          </div>
          <div>
            <span style={{ color: 'var(--accent-amber)' }}>⚠️ Educational Use Only</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
