import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Layout.css';

const Layout = ({ children }) => {
  const navigate = useNavigate();
  const [showAccountSwitcher, setShowAccountSwitcher] = useState(false);
  const switcherRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (switcherRef.current && !switcherRef.current.contains(event.target)) {
        setShowAccountSwitcher(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSwitchAccountClick = (e, targetRole) => {
    e.stopPropagation(); // Prevent event from bubbling up
    
    // For demo purposes, just show an alert
    alert(`Switching to ${targetRole} account (demo)`);
    setShowAccountSwitcher(false);
  };

  const handleUserSectionClick = (e) => {
    e.stopPropagation(); // Prevent event from bubbling up
  };

  const getRoleDisplay = () => {
    return 'Administrator'; // Default to admin for demo
  };

  const getRoleColor = () => {
    return '#667eea'; // Admin color
  };

  const getRoleIcon = () => {
    return (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="8.5" cy="7" r="4"></circle>
        <line x1="20" y1="8" x2="14" y2="8"></line>
        <line x1="20" y1="12" x2="14" y2="12"></line>
      </svg>
    );
  };

  return (
    <div className="layout">
      <header className="header">
        <div className="header-container">
          <h1 className="header-title">
            <Link to="/">Student Management System</Link>
          </h1>
          <nav className="nav">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/students" className="nav-link">Students</Link>
            <Link to="/courses" className="nav-link">Courses</Link>
            <Link to="/enrollments" className="nav-link">Enrollments</Link>
          </nav>
          <div className="user-section">
            <div className="user-info" onClick={handleUserSectionClick}>
              {getRoleIcon()}
              <div className="user-details">
                <span className="username">Admin User</span>
                <span className="user-role" style={{ color: getRoleColor() }}>
                  {getRoleDisplay()}
                </span>
              </div>
              <svg 
                width="12" 
                height="12" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2"
                className={`dropdown-arrow ${showAccountSwitcher ? 'open' : ''}`}
              >
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </div>
            
            {/* Account Switcher Dropdown */}
            {showAccountSwitcher && (
              <div className="account-switcher" ref={switcherRef}>
                <div className="switcher-header">
                  <h4>Switch Account</h4>
                  <button 
                    onClick={() => setShowAccountSwitcher(false)}
                    className="close-switcher"
                  >
                    ×
                  </button>
                </div>
                
                <div className="switcher-options">
                  <button
                    onClick={(e) => handleSwitchAccountClick(e, 'admin')}
                    className={`switcher-option current`}
                  >
                    <div className="option-icon admin-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="8.5" cy="7" r="4"></circle>
                        <line x1="20" y1="8" x2="14" y2="8"></line>
                        <line x1="20" y1="12" x2="14" y2="12"></line>
                      </svg>
                    </div>
                    <div className="option-content">
                      <div className="option-name">Admin User</div>
                      <div className="option-role">Administrator</div>
                    </div>
                    <div className="option-badge">Current</div>
                  </button>
                  
                  <button
                    onClick={(e) => handleSwitchAccountClick(e, 'staff')}
                    className="switcher-option"
                  >
                    <div className="option-icon staff-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                      </svg>
                    </div>
                    <div className="option-content">
                      <div className="option-name">Staff User</div>
                      <div className="option-role">Staff Member</div>
                    </div>
                  </button>
                </div>
                
                <div className="switcher-footer">
                  <button className="logout-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                      <polyline points="16,17 21,12 16,7"></polyline>
                      <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                    Logout
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="main">
        <div className="container">
          {children}
        </div>
      </main>

      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2024 Student Management System. Built with React & FastAPI.</p>
          <div className="footer-links">
            <span>Version 1.0.0</span>
            <span>|</span>
            <span>Professional Edition</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
