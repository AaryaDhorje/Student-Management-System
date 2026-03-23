import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import './EnrollmentsPage.css';

const EnrollmentsPage = () => {
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showEnrollForm, setShowEnrollForm] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showDeletedModal, setShowDeletedModal] = useState(false);
  const [deletedEnrollments, setDeletedEnrollments] = useState([]);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch students and courses first
      const [studentsResponse, coursesResponse] = await Promise.all([
        apiService.getStudents(1, 100),
        apiService.getCourses(1, 100)
      ]);
      
      const studentsData = studentsResponse?.data || [];
      const coursesData = coursesResponse?.data || [];
      
      console.log('Students data:', studentsData);
      console.log('Courses data:', coursesData);
      
      setStudents(studentsData);
      setCourses(coursesData);
      
      // Then fetch enrollments for each student
      const allEnrollments = [];
      
      for (const student of studentsData) {
        try {
          console.log(`Fetching enrollments for student ${student.id}...`);
          const studentEnrollments = await apiService.getStudentCourses(student.id);
          console.log(`Student ${student.id} enrollments response:`, studentEnrollments);
          
          // Handle different response structures
          let enrollmentsData = [];
          if (Array.isArray(studentEnrollments)) {
            enrollmentsData = studentEnrollments;
          } else if (studentEnrollments?.data && Array.isArray(studentEnrollments.data)) {
            enrollmentsData = studentEnrollments.data;
          } else if (studentEnrollments?.courses && Array.isArray(studentEnrollments.courses)) {
            enrollmentsData = studentEnrollments.courses;
          }
          
          console.log(`Processed enrollments for student ${student.id}:`, enrollmentsData);
          
          if (enrollmentsData.length > 0) {
            enrollmentsData.forEach(enrollment => {
              // Find course details
              const course = coursesData.find(c => c.id === enrollment.course_id || c.id === enrollment.id);
              
              allEnrollments.push({
                student_id: student.id,
                student_name: `${student.first_name} ${student.last_name}`,
                student_email: student.email,
                course_id: enrollment.course_id || enrollment.id,
                course_name: course?.course_name || enrollment.course_name || 'Unknown Course',
                course_code: course?.course_code || enrollment.course_code || 'N/A',
                enrollment_date: enrollment.enrollment_date || enrollment.created_at || new Date().toISOString()
              });
            });
          }
        } catch (err) {
          console.error(`Error fetching enrollments for student ${student.id}:`, err);
          // Continue with other students even if one fails
        }
      }
      
      console.log('All processed enrollments:', allEnrollments);
      setEnrollments(allEnrollments);
    } catch (err) {
      console.error('Error fetching initial data:', err);
      setError('Failed to load data: ' + (err.message || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  const handleEnrollStudent = () => {
    setSelectedStudent(null);
    setSelectedCourse(null);
    setShowEnrollForm(true);
  };

  const handleRemoveEnrollment = async (studentId, courseId) => {
    if (window.confirm('Are you sure you want to remove this enrollment? This can be restored later.')) {
      try {
        await apiService.removeEnrollment(studentId, courseId);
        await fetchInitialData(); // Refresh the list
      } catch (err) {
        console.error('Error removing enrollment:', err);
        setError('Failed to remove enrollment: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const handleRestoreEnrollment = async (studentId, courseId) => {
    if (window.confirm('Are you sure you want to restore this enrollment?')) {
      try {
        await apiService.restoreEnrollment(studentId, courseId);
        await fetchInitialData(); // Refresh active enrollments
        await fetchDeletedEnrollments(); // Refresh deleted enrollments
      } catch (err) {
        console.error('Error restoring enrollment:', err);
        setError('Failed to restore enrollment: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const handleHardRemoveEnrollment = async (studentId, courseId) => {
    if (window.confirm('Are you sure you want to permanently remove this enrollment? This action cannot be undone!')) {
      try {
        await apiService.hardRemoveEnrollment(studentId, courseId);
        await fetchDeletedEnrollments(); // Refresh deleted enrollments
      } catch (err) {
        console.error('Error permanently removing enrollment:', err);
        setError('Failed to permanently remove enrollment: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const fetchDeletedEnrollments = async () => {
    try {
      const response = await apiService.getDeletedEnrollments(1, 100);
      if (response && response.data) {
        setDeletedEnrollments(response.data);
      } else {
        setDeletedEnrollments([]);
      }
    } catch (err) {
      console.error('Error fetching deleted enrollments:', err);
      setDeletedEnrollments([]);
    }
  };

  const toggleDeletedModal = () => {
    if (!showDeletedModal) {
      fetchDeletedEnrollments();
    }
    setShowDeletedModal(!showDeletedModal);
  };

  const handleEnrollSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedStudent || !selectedCourse) {
      setError('Please select both a student and a course');
      return;
    }
    
    try {
      setError(null);
      console.log('Enrolling student:', selectedStudent, 'in course:', selectedCourse);
      
      // Check if student is already enrolled in this course
      const existingEnrollment = enrollments.find(
        enrollment => 
          enrollment.student_id === selectedStudent && 
          enrollment.course_id === selectedCourse
      );
      
      if (existingEnrollment) {
        setError('This student is already enrolled in this course. Please choose a different course or student.');
        return;
      }
      
      await apiService.enrollStudent(selectedStudent, { course_id: selectedCourse });
      console.log('Enrollment successful!');
      
      setShowEnrollForm(false);
      setSelectedStudent(null);
      setSelectedCourse(null);
      
      // Wait a moment before refreshing to ensure backend has processed
      setTimeout(() => {
        fetchInitialData();
      }, 500);
      
    } catch (err) {
      console.error('Error enrolling student:', err);
      
      // Handle specific error cases
      if (err.message.includes('HTTP error! status: 409')) {
        setError('This student is already enrolled in this course. Please choose a different course or student.');
      } else if (err.message.includes('HTTP error! status: 404')) {
        setError('Student or course not found. Please refresh the page and try again.');
      } else if (err.message.includes('HTTP error! status: 400')) {
        setError('Invalid enrollment data. Please check your selection and try again.');
      } else {
        setError('Failed to enroll student: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const handleEnrollCancel = () => {
    setShowEnrollForm(false);
    setSelectedStudent(null);
    setSelectedCourse(null);
    setError(null);
  };

  // Filter enrollments based on search term
  const filteredEnrollments = enrollments.filter(enrollment =>
    enrollment.student_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (enrollment.student_email && enrollment.student_email.toLowerCase().includes(searchTerm.toLowerCase())) ||
    enrollment.course_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    enrollment.course_code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (showEnrollForm) {
    return (
      <div className="enrollments-page">
        <div className="page-header">
          <h1>Enroll Student in Course</h1>
          <button onClick={handleEnrollCancel} className="btn btn-secondary">
            Cancel
          </button>
        </div>

        {error && (
          <div className="error-message">
            {error}
            <button onClick={() => setError(null)} className="close-error">×</button>
          </div>
        )}

        <div className="enroll-form">
          <form onSubmit={handleEnrollSubmit} className="form">
            <div className="form-group">
              <label htmlFor="student">Select Student *</label>
              <select
                id="student"
                value={selectedStudent || ''}
                onChange={(e) => {
                  setSelectedStudent(parseInt(e.target.value));
                  setSelectedCourse(null); // Reset course when student changes
                }}
                required
              >
                <option value="">Choose a student...</option>
                {students.map(student => (
                  <option key={student.id} value={student.id}>
                    {student.first_name} {student.last_name} ({student.email})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="course">Select Course *</label>
              <select
                id="course"
                value={selectedCourse || ''}
                onChange={(e) => setSelectedCourse(parseInt(e.target.value))}
                required
                disabled={!selectedStudent}
              >
                <option value="">Choose a course...</option>
                {courses.map(course => {
                  const isEnrolled = selectedStudent && enrollments.some(
                    enrollment => 
                      enrollment.student_id === selectedStudent && 
                      enrollment.course_id === course.id
                  );
                  return (
                    <option 
                      key={course.id} 
                      value={course.id}
                      disabled={isEnrolled}
                    >
                      {course.course_name} ({course.course_code})
                      {isEnrolled && ' - Already Enrolled'}
                    </option>
                  );
                })}
              </select>
              {selectedStudent && (
                <small className="form-help">
                  💡 Courses marked as "Already Enrolled" cannot be selected again.
                </small>
              )}
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                Enroll Student
              </button>
              <button type="button" onClick={handleEnrollCancel} className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="enrollments-page">
      <div className="page-header">
        <h1>Enrollments</h1>
        <div className="header-actions">
          <button onClick={fetchInitialData} className="btn btn-secondary" title="Refresh data">
            🔄 Refresh
          </button>
          <button onClick={toggleDeletedModal} className="btn btn-secondary">
            🗑️ View Deleted
          </button>
          <button onClick={handleEnrollStudent} className="btn btn-primary">
            Enroll Student
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError(null)} className="close-error">×</button>
        </div>
      )}

      <div className="stats-bar">
        <div className="stat-item">
          <strong>Total Enrollments:</strong> {enrollments.length}
        </div>
        <div className="stat-item">
          <strong>Students:</strong> {students.length}
        </div>
        <div className="stat-item">
          <strong>Courses:</strong> {courses.length}
        </div>
      </div>

      {/* Debug Information */}
      {process.env.NODE_ENV === 'development' && (
        <div className="debug-info" style={{ 
          background: '#f8f9fa', 
          padding: '1rem', 
          margin: '1rem 0', 
          borderRadius: '8px',
          fontSize: '0.875rem',
          fontFamily: 'monospace'
        }}>
          <h4>Debug Information:</h4>
          <div><strong>Students Found:</strong> {students.length}</div>
          <div><strong>Courses Found:</strong> {courses.length}</div>
          <div><strong>Enrollments Found:</strong> {enrollments.length}</div>
          {students.length > 0 && (
            <div><strong>Sample Student:</strong> {JSON.stringify(students[0], null, 2)}</div>
          )}
          {courses.length > 0 && (
            <div><strong>Sample Course:</strong> {JSON.stringify(courses[0], null, 2)}</div>
          )}
          {enrollments.length > 0 && (
            <div><strong>Sample Enrollment:</strong> {JSON.stringify(enrollments[0], null, 2)}</div>
          )}
        </div>
      )}

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search enrollments by student name, email, or course..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {loading && <div className="loading">Loading enrollments...</div>}

      {!loading && !error && (
        <>
          <div className="enrollments-table">
            <table>
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Email</th>
                  <th>Course</th>
                  <th>Course Code</th>
                  <th>Enrollment Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredEnrollments.map((enrollment, index) => (
                  <tr key={`${enrollment.student_id}-${enrollment.course_id}-${index}`}>
                    <td>
                      <div className="student-info">
                        <strong>{enrollment.student_name}</strong>
                      </div>
                    </td>
                    <td>{enrollment.student_email || '-'}</td>
                    <td>
                      <div className="course-info">
                        <strong>{enrollment.course_name}</strong>
                      </div>
                    </td>
                    <td>
                      <span className="course-code">{enrollment.course_code}</span>
                    </td>
                    <td>
                      {enrollment.enrollment_date ? 
                        new Date(enrollment.enrollment_date).toLocaleDateString() : 
                        new Date().toLocaleDateString()
                      }
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          onClick={() => handleRemoveEnrollment(
                            enrollment.student_id, 
                            enrollment.course_id
                          )}
                          className="btn btn-sm btn-danger"
                        >
                          Remove
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredEnrollments.length === 0 && (
            <div className="no-data">
              No enrollments found. {searchTerm ? 'Try a different search term.' : 'Enroll students in courses to get started.'}
              {!searchTerm && students.length > 0 && courses.length > 0 && (
                <div style={{ marginTop: '1rem' }}>
                  <small>
                    💡 Tip: Click "Enroll Student" to create enrollments, or click "🔄 Refresh" if you recently added enrollments.
                  </small>
                </div>
              )}
            </div>
          )}
        </>
      )}

      {/* Deleted Enrollments Modal */}
      {showDeletedModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Deleted Enrollments</h2>
              <button onClick={toggleDeletedModal} className="modal-close">×</button>
            </div>
            
            <div className="modal-body">
              {deletedEnrollments.length === 0 ? (
                <p>No deleted enrollments found.</p>
              ) : (
                <div className="deleted-enrollments-table">
                  <table>
                    <thead>
                      <tr>
                        <th>Student</th>
                        <th>Course</th>
                        <th>Enrollment Date</th>
                        <th>Deleted At</th>
                        <th>Deleted By</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {deletedEnrollments.map(enrollment => (
                        <tr key={`${enrollment.student_id}-${enrollment.course_id}`}>
                          <td>
                            {enrollment.first_name} {enrollment.last_name}
                            <br />
                            <small>{enrollment.email}</small>
                          </td>
                          <td>
                            {enrollment.course_name}
                            <br />
                            <small>{enrollment.course_code}</small>
                          </td>
                          <td>
                            {enrollment.created_at ? 
                              new Date(enrollment.created_at).toLocaleDateString() : 
                              'N/A'
                            }
                          </td>
                          <td>
                            {enrollment.deleted_at ? 
                              new Date(enrollment.deleted_at).toLocaleString() : 
                              'N/A'
                            }
                          </td>
                          <td>{enrollment.deleted_by || 'N/A'}</td>
                          <td>
                            <div className="action-buttons">
                              <button
                                onClick={() => handleRestoreEnrollment(
                                  enrollment.student_id, 
                                  enrollment.course_id
                                )}
                                className="btn btn-sm btn-success"
                                title="Restore Enrollment"
                              >
                                ↩️ Restore
                              </button>
                              <button
                                onClick={() => handleHardRemoveEnrollment(
                                  enrollment.student_id, 
                                  enrollment.course_id
                                )}
                                className="btn btn-sm btn-danger"
                                title="Permanently Remove"
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

export default EnrollmentsPage;
