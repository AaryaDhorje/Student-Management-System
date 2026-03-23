import authService from './auth';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers,
      },
      mode: 'cors',
      credentials: 'omit',
      ...options,
    };

    try {
      console.log(`Making API request to: ${url}`);
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(`API response from ${url}:`, data);
      return data;
    } catch (error) {
      console.error(`API request failed for ${url}:`, error);
      
      // Add more detailed error information
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the backend server. Please ensure the backend is running on http://127.0.0.1:8000');
      }
      
      throw error;
    }
  }

  // Student API methods
  async getStudents(page = 1, pageSize = 10) {
    return this.request(`/students?page=${page}&page_size=${pageSize}`);
  }

  async getStudent(studentId) {
    return this.request(`/students/${studentId}`);
  }

  async createStudent(studentData) {
    return this.request('/students', {
      method: 'POST',
      body: JSON.stringify(studentData),
    });
  }

  async updateStudent(studentId, studentData) {
    return this.request(`/students/${studentId}`, {
      method: 'PUT',
      body: JSON.stringify(studentData),
    });
  }

  async deleteStudent(studentId) {
    return this.request(`/students/${studentId}`, {
      method: 'DELETE',
    });
  }

  async restoreStudent(studentId) {
    return this.request(`/students/${studentId}/restore`, {
      method: 'POST',
    });
  }

  async getDeletedStudents(page = 1, pageSize = 10) {
    return this.request(`/students/deleted/list?page=${page}&page_size=${pageSize}`);
  }

  async hardDeleteStudent(studentId) {
    return this.request(`/students/${studentId}/hard`, {
      method: 'DELETE',
    });
  }

  async searchStudents(query, page = 1, pageSize = 10) {
    return this.request(`/students/search?q=${encodeURIComponent(query)}&page=${page}&page_size=${pageSize}`);
  }

  // Course API methods
  async getCourses() {
    return this.request('/courses');
  }

  async getCourse(courseId) {
    return this.request(`/courses/${courseId}`);
  }

  async createCourse(courseData) {
    return this.request('/courses', {
      method: 'POST',
      body: JSON.stringify(courseData),
    });
  }

  async updateCourse(courseId, courseData) {
    return this.request(`/courses/${courseId}`, {
      method: 'PUT',
      body: JSON.stringify(courseData),
    });
  }

  async deleteCourse(courseId) {
    return this.request(`/courses/${courseId}`, {
      method: 'DELETE',
    });
  }

  async restoreCourse(courseId) {
    return this.request(`/courses/${courseId}/restore`, {
      method: 'POST',
    });
  }

  async getDeletedCourses(page = 1, pageSize = 10) {
    return this.request(`/courses/deleted/list?page=${page}&page_size=${pageSize}`);
  }

  async hardDeleteCourse(courseId) {
    return this.request(`/courses/${courseId}/hard`, {
      method: 'DELETE',
    });
  }

  // Enrollment API methods
  async getStudentCourses(studentId) {
    return this.request(`/students/${studentId}/courses`);
  }

  async enrollStudent(studentId, courseData) {
    return this.request(`/students/${studentId}/courses`, {
      method: 'POST',
      body: JSON.stringify(courseData),
    });
  }

  async removeEnrollment(studentId, courseId) {
    return this.request(`/students/${studentId}/courses/${courseId}`, {
      method: 'DELETE',
    });
  }

  async restoreEnrollment(studentId, courseId) {
    return this.request(`/students/${studentId}/courses/${courseId}/restore`, {
      method: 'POST',
    });
  }

  async getDeletedEnrollments(page = 1, pageSize = 10) {
    return this.request(`/students/enrollments/deleted/list?page=${page}&page_size=${pageSize}`);
  }

  async hardRemoveEnrollment(studentId, courseId) {
    return this.request(`/students/${studentId}/courses/${courseId}/hard`, {
      method: 'DELETE',
    });
  }

  // Health check
  async healthCheck() {
    try {
      const response = await fetch('http://127.0.0.1:8000/health');
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
}

// Create a singleton instance
const apiService = new ApiService();

export default apiService;
