import React, { useState, useEffect } from 'react';
import CourseForm from '../components/CourseForm';
import apiService from '../services/api';
import './CoursesPage.css';

const CoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingCourse, setEditingCourse] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showDeletedModal, setShowDeletedModal] = useState(false);
  const [deletedCourses, setDeletedCourses] = useState([]);

  useEffect(() => {
    fetchCourses();
  }, [currentPage, searchTerm]);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getCourses(currentPage, 10);
      
      if (response && response.data) {
        setCourses(response.data);
        if (response.meta) {
          setTotalPages(Math.ceil(response.meta.total_records / 10));
        }
      } else {
        setCourses([]);
      }
    } catch (err) {
      console.error('Error fetching courses:', err);
      setError('Failed to fetch courses: ' + (err.message || 'Unknown error'));
      setCourses([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAddCourse = () => {
    setEditingCourse(null);
    setShowForm(true);
  };

  const handleEditCourse = (course) => {
    setEditingCourse(course);
    setShowForm(true);
  };

  const handleDeleteCourse = async (courseId) => {
    if (window.confirm('Are you sure you want to delete this course? This can be restored later.')) {
      try {
        await apiService.deleteCourse(courseId);
        await fetchCourses(); // Refresh the list
      } catch (err) {
        console.error('Error deleting course:', err);
        setError('Failed to delete course: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const handleRestoreCourse = async (courseId) => {
    if (window.confirm('Are you sure you want to restore this course?')) {
      try {
        await apiService.restoreCourse(courseId);
        await fetchCourses(); // Refresh active courses
        await fetchDeletedCourses(); // Refresh deleted courses
      } catch (err) {
        console.error('Error restoring course:', err);
        setError('Failed to restore course: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const handleHardDeleteCourse = async (courseId) => {
    if (window.confirm('Are you sure you want to permanently delete this course? This action cannot be undone!')) {
      try {
        await apiService.hardDeleteCourse(courseId);
        await fetchDeletedCourses(); // Refresh deleted courses
      } catch (err) {
        console.error('Error permanently deleting course:', err);
        setError('Failed to permanently delete course: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const fetchDeletedCourses = async () => {
    try {
      const response = await apiService.getDeletedCourses(1, 100);
      if (response && response.data) {
        setDeletedCourses(response.data);
      } else {
        setDeletedCourses([]);
      }
    } catch (err) {
      console.error('Error fetching deleted courses:', err);
      setDeletedCourses([]);
    }
  };

  const toggleDeletedModal = () => {
    if (!showDeletedModal) {
      fetchDeletedCourses();
    }
    setShowDeletedModal(!showDeletedModal);
  };

  const handleFormSubmit = async (formData) => {
    try {
      setError(null);
      
      if (editingCourse) {
        // Update existing course
        await apiService.updateCourse(editingCourse.id, formData);
      } else {
        // Add new course
        await apiService.createCourse(formData);
      }
      
      setShowForm(false);
      setEditingCourse(null);
      await fetchCourses(); // Refresh the list
    } catch (err) {
      console.error('Error saving course:', err);
      setError('Failed to save course: ' + (err.message || 'Unknown error'));
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingCourse(null);
    setError(null);
  };

  // Filter courses based on search term
  const filteredCourses = courses.filter(course =>
    course.course_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.course_code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (course.description && course.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  if (showForm) {
    return (
      <CourseForm
        course={editingCourse}
        onSubmit={handleFormSubmit}
        onCancel={handleFormCancel}
      />
    );
  }

  return (
    <div className="courses-page">
      <div className="page-header">
        <h1>Courses</h1>
        <div className="header-actions">
          <button onClick={toggleDeletedModal} className="btn btn-secondary">
            🗑️ View Deleted
          </button>
          <button onClick={handleAddCourse} className="btn btn-primary">
            Add New Course
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError(null)} className="close-error">×</button>
        </div>
      )}

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search courses by name, code, or description..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {loading && <div className="loading">Loading courses...</div>}

      {!loading && !error && (
        <>
          <div className="courses-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Course Name</th>
                  <th>Course Code</th>
                  <th>Description</th>
                  <th>Created Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredCourses.map(course => (
                  <tr key={course.id}>
                    <td>{course.id}</td>
                    <td>{course.course_name}</td>
                    <td>
                      <span className="course-code">{course.course_code}</span>
                    </td>
                    <td>
                      <div className="description">
                        {course.description || '-'}
                      </div>
                    </td>
                    <td>{new Date(course.created_at).toLocaleDateString()}</td>
                    <td>
                      <div className="action-buttons">
                        <button
                          onClick={() => handleEditCourse(course)}
                          className="btn btn-sm btn-secondary"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteCourse(course.id)}
                          className="btn btn-sm btn-danger"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredCourses.length === 0 && (
            <div className="no-data">
              No courses found. {searchTerm ? 'Try a different search term.' : 'Add your first course to get started.'}
            </div>
          )}

          {totalPages > 1 && (
            <div className="pagination">
              <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="btn btn-secondary"
              >
                Previous
              </button>
              <span className="page-info">
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className="btn btn-secondary"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}

      {/* Deleted Courses Modal */}
      {showDeletedModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Deleted Courses</h2>
              <button onClick={toggleDeletedModal} className="modal-close">×</button>
            </div>
            
            <div className="modal-body">
              {deletedCourses.length === 0 ? (
                <p>No deleted courses found.</p>
              ) : (
                <div className="deleted-courses-table">
                  <table>
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Course Name</th>
                        <th>Course Code</th>
                        <th>Description</th>
                        <th>Deleted At</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {deletedCourses.map(course => (
                        <tr key={course.id}>
                          <td>{course.id}</td>
                          <td>{course.course_name}</td>
                          <td>{course.course_code}</td>
                          <td>{course.description || 'N/A'}</td>
                          <td>
                            {course.deleted_at ? 
                              new Date(course.deleted_at).toLocaleString() : 
                              'N/A'
                            }
                          </td>
                          <td>
                            <div className="action-buttons">
                              <button
                                onClick={() => handleRestoreCourse(course.id)}
                                className="btn btn-sm btn-success"
                                title="Restore Course"
                              >
                                ↩️ Restore
                              </button>
                              <button
                                onClick={() => handleHardDeleteCourse(course.id)}
                                className="btn btn-sm btn-danger"
                                title="Permanently Delete"
                              >
                                🗑️ Delete Forever
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CoursesPage;
