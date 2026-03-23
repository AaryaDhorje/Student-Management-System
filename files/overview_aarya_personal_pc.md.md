# Student Management System --- Overview

## Problem Statement

Educational institutions often manage student information using
spreadsheets or disconnected tools, which can lead to inconsistent data,
manual errors, and inefficient administrative workflows. Managing
student records and course enrollments becomes difficult when
information is scattered across multiple systems.

The Student Management System (SMS) addresses this problem by providing
a centralized platform that allows internal staff to manage student
records and course enrollments in a structured and reliable way.

## Target Users

**Admin Staff**\
Administrative staff responsible for maintaining student and course
information. Their goal is to manage records efficiently, ensure data
accuracy, and oversee the assignment of students to courses.

**Academic Staff**\
Operational staff who primarily interact with student data for
day-to-day academic coordination. Their goal is to view student
information and assign students to courses without modifying core
records.

## Key Capabilities

-   Create, update, and deactivate student records
-   Manage course information within the institution
-   Assign students to one or more courses
-   View lists of students and course enrollments
-   Maintain structured and consistent academic records
-   Support role-based access for administrative and operational staff

## Scope Boundaries

**In Scope** - Managing student records within the institution -
Managing course information - Assigning and removing course
enrollments - Internal access for administrative and academic staff

**Out of Scope** - Student self-service portals - Payment or billing
systems - Attendance tracking - Notification systems such as email or
SMS - Mobile applications - Advanced analytics or reporting tools

## Assumptions

-   Course enrollments are dynamic, meaning students are assigned to
    courses by staff as needed.
-   The system is expected to be primarily read-oriented, where users
    frequently view student and course information.
-   Student deletion is handled through a soft-deactivation approach to
    preserve historical records.
-   The system will initially support a single institution rather than
    multiple organizations.

## Non-Goals (v1)

-   Payment processing or billing features
-   Attendance tracking capabilities
-   Notification systems (email, SMS, push notifications)
-   Mobile applications
-   Student login or self-service access

## Success Criteria

-   Staff can successfully create, update, and deactivate student
    records
-   Courses can be created and managed reliably
-   Students can be assigned to and removed from courses without data
    inconsistencies
-   Administrative staff can view organized lists of students and
    enrollments
-   The system consistently maintains accurate and structured academic
    records
