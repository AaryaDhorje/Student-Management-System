import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import authService from '../services/auth';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication status on component mount
    const initAuth = async () => {
      if (authService.isAuthenticated()) {
        try {
          // Verify token with backend
          const isValid = await authService.verifyToken();
          if (isValid) {
            const user = authService.getUser();
            setIsAuthenticated(true);
            setUser(user.username);
            setRole(user.role);
          } else {
            // Token is invalid, clear it
            authService.logout();
          }
        } catch (error) {
          console.error('Auth initialization error:', error);
          authService.logout();
        }
      }
      
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (username, password) => {
    try {
      console.log('🔐 AuthContext.login called with:', { username, password: '***' });
      await authService.login(username, password);
      const user = authService.getUser();
      console.log('🔐 AuthContext.login - user from authService:', user);
      setIsAuthenticated(true);
      setUser(user.username);
      setRole(user.role);
      console.log('🔐 AuthContext.login - state updated:', { isAuthenticated: true, user: user.username, role: user.role });
    } catch (error) {
      console.error('🔐 AuthContext.login error:', error);
      throw error;
    }
  };

  const logout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setUser(null);
    setRole(null);
  };

  // Stable value object with dependencies
  const contextValue = React.useMemo(() => ({
    isAuthenticated,
    user,
    role,
    loading,
    login,
    logout,
    isAdmin: authService.isAdmin(),
    isStaff: authService.isStaff(),
    getFullName: authService.getFullName(),
    getRoleDisplay: authService.getRoleDisplay(),
  }), [isAuthenticated, user, role, loading]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Protected Route Component
export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  console.log('🛡️ ProtectedRoute - state:', { isAuthenticated, loading, location: location.pathname });

  useEffect(() => {
    console.log('🛡️ ProtectedRoute useEffect - checking auth:', { isAuthenticated, loading });
    if (!loading && !isAuthenticated) {
      console.log('🛡️ ProtectedRoute - redirecting to login');
      navigate('/login', { replace: true, state: { from: location } });
    }
  }, [isAuthenticated, loading, navigate, location]);

  if (loading) {
    console.log('🛡️ ProtectedRoute - showing loading');
    return (
      <div className="loading-page">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Authenticating...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    console.log('🛡️ ProtectedRoute - not authenticated, returning null');
    return null; // Will redirect due to useEffect
  }

  console.log('🛡️ ProtectedRoute - rendering children');
  return children;
};
