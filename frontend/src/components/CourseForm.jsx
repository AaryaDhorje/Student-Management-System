import React, { useState } from 'react';
import './CourseForm.css';

const CourseForm = ({ course, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    course_name: course?.course_name || '',
    course_code: course?.course_code || '',
    description: course?.description || ''
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.course_name.trim()) {
      newErrors.course_name = 'Course name is required';
    }
    
    if (!formData.course_code.trim()) {
      newErrors.course_code = 'Course code is required';
    } else if (formData.course_code.length < 3) {
      newErrors.course_code = 'Course code must be at least 3 characters';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="course-form">
      <h2>{course ? 'Edit Course' : 'Add New Course'}</h2>
      
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="course_name">Course Name *</label>
          <input
            type="text"
            id="course_name"
            name="course_name"
            value={formData.course_name}
            onChange={handleChange}
            className={errors.course_name ? 'error' : ''}
            placeholder="Enter course name"
          />
          {errors.course_name && <span className="error-message">{errors.course_name}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="course_code">Course Code *</label>
          <input
            type="text"
            id="course_code"
            name="course_code"
            value={formData.course_code}
            onChange={handleChange}
            className={errors.course_code ? 'error' : ''}
            placeholder="Enter course code (e.g., CS101)"
          />
          {errors.course_code && <span className="error-message">{errors.course_code}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Enter course description"
            rows="4"
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            {course ? 'Update Course' : 'Add Course'}
          </button>
          <button type="button" onClick={onCancel} className="btn btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default CourseForm;
