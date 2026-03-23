# Student Management System --- BACKLOG.md

## 1. Epics

**Epic 1: Student Management** Focuses on creating, updating,
retrieving, and deactivating student records.

**Epic 2: Course Management** Focuses on managing course information
available within the institution.

**Epic 3: Enrollment Management** Focuses on assigning students to
courses and managing enrollment records.

------------------------------------------------------------------------

# Epic 1 --- Student Management

### US-01: Create Student

**As an** admin user\
**I want to** create a new student record\
**So that** the institution can maintain structured student information

**Acceptance Criteria** - AC-01-1: Returns success when a student record
is created with valid fields - AC-01-2: Returns an error if email
already exists - AC-01-3: Returns an error if required fields
(first_name, last_name, email) are missing - AC-01-4: Returns an error
if request data format is invalid

**Priority:** P0\
**Depends on:** None

### US-02: View Students

**As a** staff user\
**I want to** view the list of students\
**So that** I can access student information for operational tasks

**Acceptance Criteria** - AC-02-1: Returns a list of students
successfully - AC-02-2: Returns an empty list if no students exist -
AC-02-3: Returns an error if the request is unauthorized

**Priority:** P0\
**Depends on:** US-01

### US-03: Update Student

**As an** admin user\
**I want to** update an existing student record\
**So that** student information remains accurate

**Acceptance Criteria** - AC-03-1: Returns success when student record
is updated - AC-03-2: Returns an error if student does not exist -
AC-03-3: Returns an error if updated email duplicates another record -
AC-03-4: Returns an error if request data is invalid

**Priority:** P0\
**Depends on:** US-01

### US-04: Deactivate Student

**As an** admin user\
**I want to** deactivate a student record\
**So that** the student is no longer active but historical data remains

**Acceptance Criteria** - AC-04-1: Returns success when student is
marked inactive - AC-04-2: Returns an error if student does not exist -
AC-04-3: Deactivated students are excluded from standard student lists

**Priority:** P0\
**Depends on:** US-01

------------------------------------------------------------------------

# Epic 2 --- Course Management

### US-05: Create Course

**As an** admin user\
**I want to** create a course record\
**So that** students can be assigned to available courses

**Acceptance Criteria** - AC-05-1: Returns success when course is
created - AC-05-2: Returns an error if required course information is
missing - AC-05-3: Returns an error if request data format is invalid

**Priority:** P0\
**Depends on:** None

### US-06: View Courses

**As a** staff user\
**I want to** view available courses\
**So that** I can assign students to appropriate courses

**Acceptance Criteria** - AC-06-1: Returns a list of courses
successfully - AC-06-2: Returns an empty list if no courses exist -
AC-06-3: Returns an error if the request is unauthorized

**Priority:** P0\
**Depends on:** US-05

### US-07: View Course Details

**As a** staff user\
**I want to** view detailed information about a course\
**So that** I understand which course I am assigning a student to

**Acceptance Criteria** - AC-07-1: Returns course details successfully -
AC-07-2: Returns an error if the course does not exist - AC-07-3:
Returns an error if the request is unauthorized

**Priority:** P1\
**Depends on:** US-05

------------------------------------------------------------------------

# Epic 3 --- Enrollment Management

### US-08: Assign Course to Student

**As a** staff user\
**I want to** assign a course to an existing student\
**So that** I can track their enrollment

**Acceptance Criteria** - AC-08-1: Returns success when enrollment is
created - AC-08-2: Returns an error if student does not exist - AC-08-3:
Returns an error if course does not exist - AC-08-4: Returns an error if
the student is already enrolled in the course - AC-08-5: Returns an
error if request data is invalid

**Priority:** P0\
**Depends on:** US-01, US-05

### US-09: View Student Enrollments

**As a** staff user\
**I want to** view courses assigned to a student\
**So that** I can verify enrollment status

**Acceptance Criteria** - AC-09-1: Returns a list of courses assigned to
the student - AC-09-2: Returns an empty list if the student has no
enrollments - AC-09-3: Returns an error if the student does not exist

**Priority:** P0\
**Depends on:** US-01, US-05, US-08

### US-10: Remove Course Enrollment

**As a** staff user\
**I want to** remove a course from a student's enrollments\
**So that** incorrect or outdated enrollments can be corrected

**Acceptance Criteria** - AC-10-1: Returns success when enrollment is
removed - AC-10-2: Returns an error if the enrollment does not exist -
AC-10-3: Returns an error if the student does not exist - AC-10-4:
Returns an error if the course does not exist

**Priority:** P1\
**Depends on:** US-08

------------------------------------------------------------------------

# PRD Cross‑Reference Check

  PRD Requirement                Covered By
  ------------------------------ ------------
  Student creation               US-01
  Student validation rules       US-01
  View student records           US-02
  Update student                 US-03
  Soft delete student            US-04
  Create course                  US-05
  View courses                   US-06
  View course details            US-07
  Assign student to course       US-08
  Prevent duplicate enrollment   US-08
  Enrollment validation rules    US-08
  View student enrollments       US-09
  Remove enrollment              US-10

All functional requirements defined in the PRD are mapped to at least
one user story. No user stories exist without a corresponding
requirement.
