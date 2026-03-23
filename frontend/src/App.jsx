import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, ProtectedRoute } from './contexts/AuthContext';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import StudentsPage from './pages/StudentsPage';
import CoursesPage from './pages/CoursesPage';
import EnrollmentsPage from './pages/EnrollmentsPage';
import LoginPage from './pages/LoginPage';
import StaffLoginPage from './pages/StaffLoginPage';
import './App.css';
import './contexts/AuthContext.css';

function App() {
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      console.log('Checking API health...');
      const response = await fetch('http://127.0.0.1:8000/health');
      console.log('Health check response:', response);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Health check data:', data);
        setApiStatus('connected');
      } else {
        console.error('Health check failed with status:', response.status);
        setApiStatus('error');
      }
    } catch (error) {
      console.error('Health check error:', error);
      setApiStatus('error');
    }
  };

  return (
    <AuthProvider>
      <Router>
        <div className="app">
          {apiStatus === 'error' && (
            <div className="api-warning">
              ⚠️ Backend API is not connected. Some features may not work properly.
            </div>
          )}
          
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/staff-login" element={<StaffLoginPage />} />
            <Route path="/" element={
              <ProtectedRoute>
                <Layout>
                  <HomePage />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/students" element={
              <ProtectedRoute>
                <Layout>
                  <StudentsPage />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/courses" element={
              <ProtectedRoute>
                <Layout>
                  <CoursesPage />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/enrollments" element={
              <ProtectedRoute>
                <Layout>
                  <EnrollmentsPage />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
