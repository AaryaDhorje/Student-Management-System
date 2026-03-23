import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../services/auth';
import './LoginPage.css';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (error) {
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    console.log('🚀 Login form submitted with:', { username: formData.username, password: '***' });
    
    if (!formData.username.trim() || !formData.password.trim()) {
      console.log('❌ Validation failed: empty fields');
      setError('Please enter both username and password');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // First test backend connection
      console.log('🔗 Testing backend connection...');
      const backendReachable = await authService.testBackendConnection();
      if (!backendReachable) {
        throw new Error('Cannot connect to backend server. Please check if the backend is running.');
      }
      
      console.log('📞 Calling authService.login...');
      const result = await authService.login(formData.username, formData.password);
      console.log('📞 Login result:', result);
      console.log('🚀 Login successful, navigating to dashboard...');
      
      // Add a small delay and check if token is stored
      await new Promise(resolve => setTimeout(resolve, 100));
      console.log('🔍 Token check after login:', authService.getToken());
      console.log('🔍 User check after login:', authService.getUser());
      console.log('🔍 Is authenticated check:', authService.isAuthenticated());
      
      // Redirect to dashboard
      console.log('🔄 Navigating to /');
      navigate('/');
    } catch (err) {
      console.error('❌ Login failed in LoginPage:', err);
      console.error('❌ Error message:', err.message);
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <div className="login-logo">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <h1>Admin Login</h1>
            <p>Student Management System</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="username">Username</label>
              <div className="input-wrapper">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="Enter your username"
                  autoComplete="username"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="input-wrapper">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                />
              </div>
            </div>

            <button 
              type="submit" 
              className="login-button"
              disabled={loading}
            >
              {loading ? (
                <div className="loading-spinner">
                  <div className="spinner"></div>
                  Signing in...
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <div className="login-footer">
            <div className="demo-credentials">
              <h3>Demo Accounts</h3>
              <div className="credential-item">
                <strong>Admin:</strong>
                <span>admin / Admin@2024Secure!</span>
              </div>
              <div className="credential-item">
                <strong>Staff:</strong>
                <span>staff / staff123</span>
              </div>
            </div>
            <div className="security-note">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              </svg>
              <span>Secure authentication with JWT tokens</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
