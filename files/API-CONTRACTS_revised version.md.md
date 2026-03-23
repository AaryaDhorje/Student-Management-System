# API-CONTRACTS.md --- Student Management System

## 1. Versioning Strategy

All API endpoints are versioned to ensure backward compatibility.

**Base version:**\
`/api/v1/`

**Format:**\
`/api/v1/<resource>`

------------------------------------------------------------------------

## 2. Base URL & Naming Conventions

**Case:** URLs use lowercase and kebab-case.\
**Nouns:** Resources use plural nouns (e.g., `/students`).\
**Data:** JSON fields use `snake_case`.

------------------------------------------------------------------------

## 3. Standard Response Envelopes

### Success Envelope

Every successful request returns a **200 OK** or **201 Created** with
this structure:

``` json
{
  "success": true,
  "data": {},
  "message": "operation successful",
  "meta": {
    "page": 1,
    "total_records": 100
  }
}
```

### Error Envelope

Every failed request returns a relevant **4xx or 5xx** code with this
structure:

``` json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human readable explanation",
    "field": "name_of_invalid_field"
  }
}
```

------------------------------------------------------------------------

## 4. Student Endpoints (Epic 1)

  Method   Endpoint                Description
  -------- ----------------------- ----------------------------------
  POST     /api/v1/students        Create a new student record
  GET      /api/v1/students        List all students (paginated)
  GET      /api/v1/students/{id}   Get specific student details
  PUT      /api/v1/students/{id}   Update existing student
  DELETE   /api/v1/students/{id}   Soft-delete / Deactivate student

------------------------------------------------------------------------

## 5. Enrollment Endpoints (Epic 3 --- Updated)

### GET /api/v1/students/{id}/courses

**Description:**\
List all courses a specific student is enrolled in.

**Success Data Object:**

``` json
[
  {
    "course_id": "uuid",
    "course_name": "Database Systems",
    "course_code": "CS301",
    "enrollment_date": "2024-02-15",
    "grade": "A"
  }
]
```

------------------------------------------------------------------------

### POST /api/v1/students/{id}/courses

**Description:**\
Enroll a student in a course.

**Request Body:**

``` json
{
  "course_id": "uuid",
  "grade": null
}
```

------------------------------------------------------------------------

## 6. Error Code Registry

  Code                HTTP Status   Description
  ------------------- ------------- --------------------------------------------
  VALIDATION_ERROR    422           Missing fields or incorrect data format
  DUPLICATE_EMAIL     409           Student email already exists in DB
  STUDENT_NOT_FOUND   404           Provided UUID does not match any record
  ALREADY_ENROLLED    409           Student is already in that specific course

------------------------------------------------------------------------

## 7. Backlog Traceability Matrix

  User Story   Method   Endpoint
  ------------ -------- -------------------------------------
  US-01        POST     /api/v1/students
  US-04        DELETE   /api/v1/students/{id}
  US-08        POST     /api/v1/students/{id}/courses
  US-10        DELETE   /api/v1/students/{id}/courses/{cid}
