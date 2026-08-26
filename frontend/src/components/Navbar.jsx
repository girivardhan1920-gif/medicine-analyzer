import React from 'react';
import { 
  Pill, 
  Search, 
  ScanLine, 
  Activity, 
  Bot, 
  History, 
  Info, 
  Sun, 
  Moon, 
  ShieldCheck,
  Menu,
  X
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, theme, toggleTheme }) {
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const navItems = [
    { id: 'home', label: 'Home', icon: Activity },
    { id: 'analyzer', label: 'Medicine Analyzer', icon: ScanLine },
    { id: 'interactions', label: 'Interaction Checker', icon: Pill },
    { id: 'assistant', label: 'AI Assistant', icon: Bot },
    { id: 'history', label: 'Search History', icon: History },
    { id: 'about', label: 'About & Safety', icon: Info },
  ];

  const handleNavClick = (id) => {
    setActiveTab(id);
    setMobileOpen(false);
  };

  return (
    <header className="navbar">
      <div className="navbar-inner">
        {/* Brand */}
        <div className="brand-logo" onClick={() => handleNavClick('home')}>
          <div className="brand-icon-wrapper">
            <Pill size={24} />
          </div>
          <div>
            <span className="brand-text">MedAnalyze AI</span>
            <span className="brand-badge">Medical AI</span>
          </div>
        </div>

        {/* Desktop Nav */}
        <nav className="nav-links">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                id={`nav-btn-${item.id}`}
                className={`nav-item ${isActive ? 'active' : ''}`}
                onClick={() => handleNavClick(item.id)}
              >
                <Icon size={16} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Right Action: Theme Switcher */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button 
            id="theme-toggle-btn"
            className="theme-toggle-btn"
            onClick={toggleTheme}
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
          >
            {theme === 'dark' ? <Sun size={18} color="#f59e0b" /> : <Moon size={18} color="#0284c7" />}
            <span style={{ fontSize: '0.8rem' }}>{theme === 'dark' ? 'Light' : 'Dark'}</span>
          </button>

          {/* Mobile hamburger */}
          <button 
            className="mobile-menu-btn"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle navigation menu"
          >
            {mobileOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileOpen && (
        <div style={{
          padding: '16px',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px'
        }}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                className={`nav-item ${isActive ? 'active' : ''}`}
                style={{ width: '100%', justifyContent: 'flex-start', padding: '12px 16px' }}
                onClick={() => handleNavClick(item.id)}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      )}
    </header>
  );
}
