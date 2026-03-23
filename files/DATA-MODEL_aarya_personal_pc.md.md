# DATA-MODEL.md --- Student Management System

## 1. Entity List

The system stores structured data for the following entities:

-   **Student** --- Represents an individual student in the institution.
-   **Course** --- Represents an academic course offered by the
    institution.
-   **Enrollment** --- Junction entity representing the relationship
    between students and courses.

The relationship between **Student** and **Course** is **many-to-many**,
implemented using the **Enrollment** junction table.

------------------------------------------------------------------------

# 2. Entity Schemas

## Students

  ----------------------------------------------------------------------------
  Column            Type           Constraints                   Notes
  ----------------- -------------- ----------------------------- -------------
  id                UUID           PRIMARY KEY                   Unique
                                                                 identifier
                                                                 for each
                                                                 student

  first_name        VARCHAR(100)   NOT NULL                      Student first
                                                                 name

  last_name         VARCHAR(100)   NOT NULL                      Student last
                                                                 name

  email             VARCHAR(255)   NOT NULL, UNIQUE              Used to
                                                                 prevent
                                                                 duplicate
                                                                 student
                                                                 records

  enrollment_date   DATE           NOT NULL                      Date student
                                                                 enrolled in
                                                                 institution

  is_active         BOOLEAN        DEFAULT TRUE                  Soft delete
                                                                 flag

  created_at        TIMESTAMP      DEFAULT CURRENT_TIMESTAMP     Record
                                                                 creation time

  updated_at        TIMESTAMP      DEFAULT CURRENT_TIMESTAMP     Updated
                                                                 whenever
                                                                 record
                                                                 changes
  ----------------------------------------------------------------------------

------------------------------------------------------------------------

## Courses

  ------------------------------------------------------------------------
  Column        Type           Constraints                   Notes
  ------------- -------------- ----------------------------- -------------
  id            UUID           PRIMARY KEY                   Unique
                                                             identifier
                                                             for each
                                                             course

  course_name   VARCHAR(150)   NOT NULL                      Course title

  course_code   VARCHAR(50)    NOT NULL, UNIQUE              Unique course
                                                             identifier

  description   TEXT           NULL                          Optional
                                                             course
                                                             description

  created_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP     Record
                                                             creation time

  updated_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP     Updated
                                                             whenever
                                                             record
                                                             changes
  ------------------------------------------------------------------------

------------------------------------------------------------------------

## Enrollments

  -----------------------------------------------------------------------
  Column        Type          Constraints                   Notes
  ------------- ------------- ----------------------------- -------------
  id            UUID          PRIMARY KEY                   Unique
                                                            identifier
                                                            for
                                                            enrollment

  student_id    UUID          FOREIGN KEY → students.id     References
                                                            student

  course_id     UUID          FOREIGN KEY → courses.id      References
                                                            course

  created_at    TIMESTAMP     DEFAULT CURRENT_TIMESTAMP     Enrollment
                                                            creation time
  -----------------------------------------------------------------------

Additional Constraint:

-   UNIQUE(student_id, course_id) --- Prevents duplicate enrollment in
    the same course.

------------------------------------------------------------------------

# 3. Relationships

Student ↔ Course is a **Many-to-Many relationship** implemented through
the **Enrollment** table.

    Students
       │
       │ 1..*
       │
    Enrollments
       │
       │ *..1
       │
    Courses

Expanded view:

    ┌───────────┐        ┌──────────────┐        ┌───────────┐
    │  Students │        │  Enrollments │        │  Courses  │
    ├───────────┤        ├──────────────┤        ├───────────┤
    │ id        │◄───────│ student_id   │        │ id        │
    │ first_nm  │        │ course_id    │──────► │ course_nm │
    │ last_nm   │        │ created_at   │        │ course_cd │
    │ email     │        │ id           │        │ desc      │
    └───────────┘        └──────────────┘        └───────────┘

------------------------------------------------------------------------

# 4. Indexing Decisions

Indexes are introduced to optimize common query patterns.

### idx_students_email

Purpose: Quickly validate duplicate student emails during creation.

Rationale: Email uniqueness checks occur frequently when new students
are created.

------------------------------------------------------------------------

### idx_enrollments_student_id

Purpose: Retrieve all courses assigned to a student.

Rationale: Enrollment lookups by student are frequent when viewing
student details.

------------------------------------------------------------------------

### idx_enrollments_course_id

Purpose: Retrieve all students enrolled in a specific course.

Rationale: Course-level queries require efficient filtering by
course_id.

------------------------------------------------------------------------

### idx_courses_course_code

Purpose: Fast lookup of courses by unique course code.

Rationale: Course codes are often used as external identifiers.

------------------------------------------------------------------------

# 5. Soft Delete Strategy

Student records implement a **soft delete mechanism** using the
`is_active` flag.

Behavior:

-   When a student is deleted, the record remains in the database.
-   `is_active` is set to FALSE.
-   Standard student queries exclude inactive students.

Rationale:

-   Preserves historical enrollment relationships
-   Prevents accidental loss of institutional records
-   Maintains referential integrity for enrollment data

Courses and enrollments do not use soft delete in version 1.

------------------------------------------------------------------------

# 6. Cascade Behavior for Relationships

The following cascade rules are applied to maintain data integrity.

### Student → Enrollment

When a student is deactivated:

-   Enrollment records remain intact for historical purposes.
-   Queries filtering active students will exclude deactivated records.

Deletion behavior: - Hard deletion of students is restricted to prevent
orphan records.

------------------------------------------------------------------------

### Course → Enrollment

If a course is removed:

-   Associated enrollments must be deleted first.

Cascade rule:

    ON DELETE CASCADE

This ensures that orphan enrollment records do not remain.

------------------------------------------------------------------------

# 7. Audit Column Strategy

All primary entities include audit columns to track record lifecycle.

  Column       Purpose
  ------------ -----------------------------------------
  created_at   Timestamp when record was created
  updated_at   Timestamp when record was last modified

Benefits:

-   Enables operational auditing
-   Supports debugging and data tracking
-   Provides foundation for future analytics

Enrollment records include `created_at` to track when a student joined a
course.

------------------------------------------------------------------------

# Summary

The data model is designed to support:

-   Reliable student record management
-   Course catalog management
-   Many-to-many student-course relationships
-   Soft deletion of students
-   Efficient enrollment queries through indexing

This schema directly supports the functional requirements defined in the
PRD and enables efficient implementation of the system architecture.
