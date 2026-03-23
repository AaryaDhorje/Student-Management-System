# QUALITY.md --- Engineering Quality Standards

## Code Review Checklist (per PR)

Before approving any pull request, reviewers must verify:

-   [ ] Response format strictly follows the standard response envelope
    defined in API-CONTRACTS.md
-   [ ] Error responses return the correct error codes defined in
    API-CONTRACTS.md
-   [ ] No raw SQLAlchemy or internal exceptions are exposed to the API
    layer
-   [ ] All request and response bodies use Pydantic schemas
-   [ ] Role-based access restrictions are enforced for protected
    operations
-   [ ] Business logic exists only in the service layer (not in routers)
-   [ ] Repository layer handles all database access
-   [ ] No hardcoded configuration values (use environment/config)
-   [ ] No print() statements --- use structured logging
-   [ ] All route handlers are asynchronous
-   [ ] File length does not exceed 200 lines
-   [ ] Code follows naming conventions defined in `.cursorrules`

------------------------------------------------------------------------

## API Consistency Checks

All API endpoints must pass the following consistency checks:

-   [ ] Every response follows the standard envelope format
-   [ ] Error responses follow the standard error envelope
-   [ ] JSON fields use snake_case
-   [ ] URLs use lowercase plural resource names
-   [ ] Pagination supported on all list endpoints
-   [ ] Pagination parameters include `page` and `page_size`
-   [ ] Pagination responses include metadata (`page`, `page_size`,
    `total`)
-   [ ] HTTP status codes align with API-CONTRACTS.md definitions
-   [ ] Endpoint naming matches the REST API design plan

------------------------------------------------------------------------

## Logging Expectations

Logging must follow these operational rules:

-   [ ] Incoming requests logged at INFO level
-   [ ] Successful create/update/delete operations logged at INFO level
-   [ ] All unhandled exceptions logged at ERROR level
-   [ ] Database failures logged at ERROR level
-   [ ] Validation failures logged with context

Logging must never include:

-   [ ] passwords
-   [ ] authentication tokens
-   [ ] personally identifiable information (PII)

------------------------------------------------------------------------

## Test Coverage Expectations

Each feature must include automated tests that cover the following
scenarios:

Student operations: - Create student successfully - Duplicate email
rejected - Missing required fields rejected - Update student
successfully - Update non-existent student returns error - Soft delete
student successfully

Course operations: - Create course successfully - Duplicate course code
rejected - Retrieve course list successfully - Retrieve non-existent
course returns error

Enrollment operations: - Assign course to student successfully - Prevent
duplicate enrollment - Reject enrollment if student does not exist -
Reject enrollment if course does not exist - Remove enrollment
successfully - Reject removal of non-existent enrollment

Authorization: - Reject requests without authentication - Reject
requests with insufficient permissions

Validation: - Reject malformed request bodies - Reject invalid
identifiers

------------------------------------------------------------------------

## Manual Test Checklist

Before marking any backlog story as complete, perform the following
manual tests:

-   [ ] Create student and verify response matches API contract
-   [ ] Attempt duplicate student creation and verify conflict error
-   [ ] Retrieve student list and confirm pagination works
-   [ ] Update student and verify changes persist
-   [ ] Soft delete student and verify record no longer appears in
    active list
-   [ ] Create course and verify retrieval
-   [ ] Assign course to student and verify enrollment appears
-   [ ] Attempt duplicate enrollment and verify conflict error
-   [ ] Remove enrollment and verify deletion
-   [ ] Attempt operations with invalid IDs and verify correct errors

------------------------------------------------------------------------

## Definition of Done

A feature is considered complete only when all conditions below are
satisfied:

1.  Implementation matches the requirements defined in PRD.md and
    BACKLOG.md.
2.  API behavior matches contracts defined in API-CONTRACTS.md.
3.  Data persistence aligns with the schema defined in DATA-MODEL.md.
4.  Architecture rules defined in ARCH.md are respected.
5.  Code passes the Code Review Checklist.
6.  Automated tests cover happy paths and error paths.
7.  Manual test checklist has been executed successfully.
8.  Logging follows project logging expectations.
9.  No linting or formatting errors exist.
10. No architectural violations exist according to `.cursorrules`.

------------------------------------------------------------------------

# Final Consistency Audit (Pre-Build Verification)

Before beginning implementation, perform a full documentation audit.

Verify the following cross-document consistency checks:

1.  **PRD ↔ BACKLOG**
    -   Every functional requirement has at least one corresponding user
        story.
    -   No backlog story exists without a corresponding PRD requirement.
2.  **BACKLOG ↔ API-CONTRACTS**
    -   Every user story is implemented through at least one API
        endpoint.
    -   No endpoint exists without a mapped user story.
3.  **DATA-MODEL ↔ API-CONTRACTS**
    -   Every response field corresponds to a column in DATA-MODEL.md.
    -   No response field exists that is not defined in the data model.
4.  **ARCH ↔ .cursorrules**
    -   Folder structure in `.cursorrules` matches the architecture
        defined in ARCH.md.
5.  **API-CONTRACTS ↔ QUALITY**
    -   Every error scenario defined in API contracts has a
        corresponding test or validation check.

Implementation must not begin until all consistency checks pass.
