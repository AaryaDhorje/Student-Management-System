// Authentication Service for Frontend
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

class AuthService {
  constructor() {
    // Clear any old auth data on initialization
    this.clearOldAuthData();
    this.token = localStorage.getItem('auth_token');
    this.user = JSON.parse(localStorage.getItem('auth_user') || 'null');
  }

  clearOldAuthData() {
    // Remove old demo auth data
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('authUser');
    localStorage.removeItem('authRole');
  }

  // Login user
  async login(username, password) {
    try {
      console.log('🔐 Attempting login with:', { username, password: '***' });
      console.log('🌐 API URL:', `${API_BASE_URL}/auth/login`);
      
      const requestBody = JSON.stringify({ username, password });
      console.log('📤 Request body:', requestBody);
      
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: requestBody,
      });

      console.log('📥 Login response status:', response.status);
      console.log('📥 Login response headers:', response.headers);
      
      if (!response.ok) {
        const error = await response.json();
        console.error('❌ Login error response:', error);
        throw new Error(error.error?.message || `Login failed with status ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Login successful:', data);
      
      // Store token and user info
      this.token = data.access_token;
      this.user = data.user;
      
      localStorage.setItem('auth_token', this.token);
      localStorage.setItem('auth_user', JSON.stringify(this.user));
      
      console.log('💾 Token stored:', this.token ? 'YES' : 'NO');
      console.log('👤 User stored:', this.user ? this.user.username : 'NONE');
      
      return data;
    } catch (error) {
      console.error('❌ Login error:', error);
      console.error('❌ Error stack:', error.stack);
      throw error;
    }
  }

  // Logout user
  logout() {
    this.token = null;
    this.user = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    // Also clear old demo data
    this.clearOldAuthData();
  }

  // Get current token
  getToken() {
    return this.token;
  }

  // Get current user
  getUser() {
    return this.user;
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.token && !!this.user;
  }

  // Check if user is admin
  isAdmin() {
    return this.user?.role === 'admin';
  }

  // Check if user is staff
  isStaff() {
    return this.user?.role === 'staff';
  }

  // Check if user has specific role
  hasRole(role) {
    return this.user?.role === role;
  }

  // Get user full name
  getFullName() {
    if (!this.user) return '';
    return `${this.user.first_name} ${this.user.last_name}`;
  }

  // Get user role display name
  getRoleDisplay() {
    if (!this.user) return '';
    return this.user.role.charAt(0).toUpperCase() + this.user.role.slice(1);
  }

  // Verify token with backend
  async verifyToken() {
    if (!this.token) return false;
    
    try {
      const response = await fetch(`${API_BASE_URL}/auth/verify-token`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        this.logout();
        return false;
      }

      const data = await response.json();
      return data.valid;
    } catch (error) {
      console.error('Token verification error:', error);
      this.logout();
      return false;
    }
  }

  // Refresh user info from backend
  async refreshUserInfo() {
    if (!this.token) return null;
    
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        this.logout();
        return null;
      }

      const user = await response.json();
      this.user = user;
      localStorage.setItem('auth_user', JSON.stringify(user));
      return user;
    } catch (error) {
      console.error('Refresh user info error:', error);
      this.logout();
      return null;
    }
  }

  // Test method to check if backend is reachable
  async testBackendConnection() {
    try {
      console.log('🔗 Testing backend connection...');
      // Test the health endpoint directly
      const response = await fetch('http://127.0.0.1:8000/health', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      console.log('🔗 Backend connection test status:', response.status);
      const data = await response.json();
      console.log('🔗 Backend connection test data:', data);
      return response.ok;
    } catch (error) {
      console.error('🔗 Backend connection test failed:', error);
      return false;
    }
  }

  // Get auth headers for API requests
  getAuthHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }
}

// Create singleton instance
const authService = new AuthService();

export default authService;
