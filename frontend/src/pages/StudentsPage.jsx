import React, { useState, useEffect } from 'react';
import StudentForm from '../components/StudentForm';
import apiService from '../services/api';
import './StudentsPage.css';

const StudentsPage = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showDeleted, setShowDeleted] = useState(false);
  const [deletedStudents, setDeletedStudents] = useState([]);
  const [showDeletedModal, setShowDeletedModal] = useState(false);

  useEffect(() => {
    fetchStudents();
  }, [currentPage, searchTerm]);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getStudents(currentPage, 10);
      
      if (response && response.data) {
        setStudents(response.data);
        if (response.meta) {
          setTotalPages(Math.ceil(response.meta.total_records / 10));
        }
      } else {
        setStudents([]);
      }
    } catch (err) {
      console.error('Error fetching students:', err);
      setError('Failed to fetch students: ' + (err.message || 'Unknown error'));
      setStudents([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAddStudent = () => {
    setEditingStudent(null);
    setShowForm(true);
  };

  const handleEditStudent = (student) => {
    setEditingStudent(student);
    setShowForm(true);
  };

  const handleDeleteStudent = async (studentId) => {
    if (window.confirm('Are you sure you want to delete this student? This can be restored later.')) {
      try {
        await apiService.deleteStudent(studentId);
        await fetchStudents(); // Refresh the list
      } catch (err) {
        console.error('Error deleting student:', err);
        setError('Failed to delete student: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const handleRestoreStudent = async (studentId) => {
    if (window.confirm('Are you sure you want to restore this student?')) {
      try {
        await apiService.restoreStudent(studentId);
        await fetchStudents(); // Refresh active students
        await fetchDeletedStudents(); // Refresh deleted students
      } catch (err) {
        console.error('Error restoring student:', err);
        setError('Failed to restore student: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const handleHardDeleteStudent = async (studentId) => {
    if (window.confirm('Are you sure you want to permanently delete this student? This action cannot be undone!')) {
      try {
        await apiService.hardDeleteStudent(studentId);
        await fetchDeletedStudents(); // Refresh deleted students
      } catch (err) {
        console.error('Error permanently deleting student:', err);
        setError('Failed to permanently delete student: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const fetchDeletedStudents = async () => {
    try {
      const response = await apiService.getDeletedStudents(1, 100);
      if (response && response.data) {
        setDeletedStudents(response.data);
      } else {
        setDeletedStudents([]);
      }
    } catch (err) {
      console.error('Error fetching deleted students:', err);
      setDeletedStudents([]);
    }
  };

  const toggleDeletedModal = () => {
    if (!showDeletedModal) {
      fetchDeletedStudents();
    }
    setShowDeletedModal(!showDeletedModal);
  };

  const handleFormSubmit = async (formData) => {
    try {
      setError(null);
      
      // Format the data for the API
      const apiData = {
        ...formData,
        enrollment_date: formData.enrollment_date
      };

      if (editingStudent) {
        // Update existing student
        await apiService.updateStudent(editingStudent.id, apiData);
      } else {
        // Add new student
        await apiService.createStudent(apiData);
      }
      
      setShowForm(false);
      setEditingStudent(null);
      await fetchStudents(); // Refresh the list
    } catch (err) {
      console.error('Error saving student:', err);
      setError('Failed to save student: ' + (err.message || 'Unknown error'));
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingStudent(null);
    setError(null);
  };

  // Filter students based on search term
  const filteredStudents = students.filter(student =>
    student.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (showForm) {
    return (
      <StudentForm
        student={editingStudent}
        onSubmit={handleFormSubmit}
        onCancel={handleFormCancel}
      />
    );
  }

  return (
    <div className="students-page">
      <div className="page-header">
        <h1>Students</h1>
        <div className="header-actions">
          <button onClick={toggleDeletedModal} className="btn btn-secondary">
            🗑️ View Deleted
          </button>
          <button onClick={handleAddStudent} className="btn btn-primary">
            Add New Student
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
          placeholder="Search students by name or email..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {loading && <div className="loading">Loading students...</div>}

      {!loading && !error && (
        <>
          <div className="students-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Enrollment Date</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredStudents.map(student => (
                  <tr key={student.id}>
                    <td>{student.id}</td>
                    <td>{`${student.first_name} ${student.last_name}`}</td>
                    <td>{student.email}</td>
                    <td>{new Date(student.enrollment_date).toLocaleDateString()}</td>
                    <td>
                      <span className={`status ${student.is_active ? 'active' : 'inactive'}`}>
                        {student.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          onClick={() => handleEditStudent(student)}
                          className="btn btn-sm btn-secondary"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteStudent(student.id)}
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

          {filteredStudents.length === 0 && (
            <div className="no-data">
              No students found. {searchTerm ? 'Try a different search term.' : 'Add your first student to get started.'}
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

      {/* Deleted Students Modal */}
      {showDeletedModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Deleted Students</h2>
              <button onClick={toggleDeletedModal} className="modal-close">×</button>
            </div>
            
            <div className="modal-body">
              {deletedStudents.length === 0 ? (
                <p>No deleted students found.</p>
              ) : (
                <div className="deleted-students-table">
                  <table>
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Deleted At</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {deletedStudents.map(student => (
                        <tr key={student.id}>
                          <td>{student.id}</td>
                          <td>{student.first_name} {student.last_name}</td>
                          <td>{student.email}</td>
                          <td>
                            {student.deleted_at ? 
                              new Date(student.deleted_at).toLocaleString() : 
                              'N/A'
                            }
                          </td>
                          <td>
                            <div className="action-buttons">
                              <button
                                onClick={() => handleRestoreStudent(student.id)}
                                className="btn btn-sm btn-success"
                                title="Restore Student"
                              >
                                ↩️ Restore
                              </button>
                              <button
                                onClick={() => handleHardDeleteStudent(student.id)}
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

export default StudentsPage;
