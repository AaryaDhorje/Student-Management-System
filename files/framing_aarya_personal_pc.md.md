# FRAMING.md

## Student Management System -- Project Framing

This document defines the scope, boundaries, assumptions, and risks of
the Student Management System (SMS). Its purpose is to ensure clarity
before system design and implementation begins, preventing scope creep
and architectural ambiguity.

------------------------------------------------------------------------

# 1. Scope Boundaries

## What the System Does

The Student Management System provides a centralized platform for
managing students and their course enrollments within an academic
institution.

Core capabilities include:

-   Managing student records
-   Managing course information
-   Assigning students to courses
-   Viewing lists of students and their enrollments
-   Role-based access for administrators and staff
-   Providing API endpoints for frontend interaction
-   Maintaining structured and consistent data in a PostgreSQL database

The system will be built using:

-   Backend: Python (FastAPI)
-   Frontend: React
-   Database: PostgreSQL

------------------------------------------------------------------------

## What the System Explicitly Does NOT Do

The system intentionally excludes the following features in Version 1:

-   Payment or billing systems
-   Attendance tracking
-   Notification systems (email/SMS)
-   Mobile applications
-   Student self-service portal
-   Advanced analytics or reporting
-   File uploads or document management

These exclusions are intentional to keep the first version focused on
core student and course management functionality.

------------------------------------------------------------------------

## Multi-Tenant Architecture

This system is single-tenant.

It is designed to support only one institution/school. There is no
separation of data across multiple schools or organizations.

Future versions may introduce multi-tenant architecture if required.

------------------------------------------------------------------------

## Admin and Staff Access

The system provides role-based access with two internal roles:

### Admin

Has full system control and can perform all operations including:

-   Create, read, update, and delete students
-   Create, read, update, and delete courses
-   Assign students to courses
-   Remove course assignments
-   View all records

### Staff

Has limited access:

-   View student records
-   View course records
-   Assign courses to students
-   Cannot delete core records

------------------------------------------------------------------------

## Student Portal

There is no student login in Version 1.

Students do not directly interact with the system. All actions are
performed internally by admin or staff users.

------------------------------------------------------------------------

# 2. Assumptions

## Course Enrollments

Course enrollments are dynamic.

This means:

-   Students can be assigned to courses at runtime.
-   Courses are created independently of students.
-   Staff or Admin can assign students to any available course.

The system must validate that:

-   The course exists
-   The student exists
-   Duplicate enrollments are prevented

------------------------------------------------------------------------

## System Load Characteristics

The system is expected to be read-heavy.

Typical usage patterns include:

-   Viewing student lists
-   Viewing course lists
-   Viewing enrollments

Write operations (creating or modifying data) will occur less
frequently.

------------------------------------------------------------------------

## Student Deletion Strategy

Student records use a soft delete strategy.

This means:

-   A student record is not permanently removed from the database.
-   Instead, a flag such as `is_deleted` or `deleted_at` marks the
    record as inactive.

This prevents accidental data loss and preserves historical data
integrity.

------------------------------------------------------------------------

# 3. Non-Goals

The following features are explicitly out of scope for this project.

Defining non-goals prevents feature creep during development.

### Payment Processing

The system will not handle tuition payments, billing, or financial
transactions.

### Attendance Tracking

Attendance monitoring and tracking are not included.

### Notification System

The system will not send: - Emails - SMS - Push notifications

### Mobile Application

Only a web application will be developed.

There will be no native Android or iOS apps.

------------------------------------------------------------------------

# 4. User Roles

## Admin

Permissions:

-   Full CRUD for students
-   Full CRUD for courses
-   Assign students to courses
-   Remove course assignments
-   View all data

Admin has the highest level of control within the system.

------------------------------------------------------------------------

## Staff

Permissions:

-   Read student data
-   Read course data
-   Assign students to courses

Restrictions:

-   Cannot delete students
-   Cannot delete courses

Staff access is designed for operational tasks without administrative
control.

------------------------------------------------------------------------

# 5. Risks

## Cascade Deletes

Deleting a student who has active course assignments may cause data
integrity issues.

Mitigation strategy:

-   Prevent deletion if active enrollments exist
-   Or automatically remove enrollments before deletion
-   Prefer soft deletes to avoid cascading failures

------------------------------------------------------------------------

## Data Integrity Risks

There is a risk of creating invalid relationships such as:

-   Enrolling a student in a non-existent course
-   Assigning duplicate enrollments

Mitigation strategy:

-   Foreign key constraints in PostgreSQL
-   Validation logic in FastAPI services
-   Unique constraints for student-course relationships

------------------------------------------------------------------------

## API Consistency Risk

During development, API routes may change while the frontend is already
integrated.

Example: Frontend calling `/students` but backend renames it to
`/api/v1/students`

Mitigation strategy:

-   Define API routes early
-   Maintain versioned API structure
-   Use consistent route naming conventions

Example:

/api/v1/students\
/api/v1/courses\
/api/v1/enrollments

------------------------------------------------------------------------

# 6. Summary

This framing document establishes the foundational boundaries of the
Student Management System.

Key characteristics:

-   Single-tenant architecture
-   Internal user roles only
-   Soft-deletion strategy
-   Dynamic course enrollment
-   Read-heavy workload
-   Minimal feature set focused on core functionality

This framing will guide the next documentation stages including:

-   OVERVIEW.md
-   ARCHITECTURE.md
-   DATA_MODEL.md
-   API_SPEC.md
-   QUALITY.md
