import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiService from '../services/api';
import './HomePage.css';

const HomePage = () => {
  const [stats, setStats] = useState({
    totalStudents: 0,
    totalCourses: 0,
    totalEnrollments: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch students count
      const studentsResponse = await apiService.getStudents(1, 1);
      const studentsCount = studentsResponse?.meta?.total_records || 0;
      
      // Fetch courses count
      const coursesResponse = await apiService.getCourses(1, 1);
      const coursesCount = coursesResponse?.meta?.total_records || 0;
      
      // For now, simulate enrollments count
      const enrollmentsCount = Math.floor(studentsCount * 1.5);
      
      setStats({
        totalStudents: studentsCount,
        totalCourses: coursesCount,
        totalEnrollments: enrollmentsCount
      });
    } catch (err) {
      console.error('Error fetching statistics:', err);
      setError('Failed to fetch statistics');
      setStats({
        totalStudents: 0,
        totalCourses: 0,
        totalEnrollments: 0
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="home-page">
        <div className="loading">
          <span>Loading dashboard...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="home-page">
        <div className="error">
          <h3>⚠️ Unable to Load Dashboard</h3>
          <p>{error}</p>
          <button onClick={fetchStats} className="btn btn-primary">
            🔄 Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="home-page fade-in">
      <div className="welcome-section">
        <h1>🎓 Student Management System</h1>
        <p>Empowering education through efficient student, course, and enrollment management</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon students">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <div className="stat-content">
            <h3>{stats.totalStudents.toLocaleString()}</h3>
            <p>Total Students</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon courses">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
          </div>
          <div className="stat-content">
            <h3>{stats.totalCourses.toLocaleString()}</h3>
            <p>Total Courses</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon enrollments">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="8.5" cy="7" r="4"></circle>
              <line x1="20" y1="8" x2="20" y2="14"></line>
              <line x1="23" y1="11" x2="17" y2="11"></line>
            </svg>
          </div>
          <div className="stat-content">
            <h3>{stats.totalEnrollments.toLocaleString()}</h3>
            <p>Total Enrollments</p>
          </div>
        </div>
      </div>

      <div className="quick-actions">
        <h2>🚀 Quick Actions</h2>
        <div className="actions-grid">
          <Link to="/students" className="action-card">
            <div className="action-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="8.5" cy="7" r="4"></circle>
                <line x1="20" y1="8" x2="20" y2="14"></line>
                <line x1="23" y1="11" x2="17" y2="11"></line>
              </svg>
            </div>
            <h3>Manage Students</h3>
            <p>Add, edit, or remove students from the system</p>
          </Link>

          <Link to="/courses" className="action-card">
            <div className="action-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
            </div>
            <h3>Manage Courses</h3>
            <p>Create and manage academic courses</p>
          </Link>

          <Link to="/enrollments" className="action-card">
            <div className="action-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="8.5" cy="7" r="4"></circle>
                <path d="M20 8v6M23 11h-6"></path>
              </svg>
            </div>
            <h3>Manage Enrollments</h3>
            <p>Enroll students in courses and track progress</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
