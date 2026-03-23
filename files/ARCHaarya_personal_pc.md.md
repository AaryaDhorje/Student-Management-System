
# ARCH.md — Student Management System Architecture

## 1. Architecture Diagram

The system follows a layered architecture to clearly separate responsibilities between presentation, business logic, and data access.

```
┌──────────────────────────────────────────┐
│             React Frontend               │
│        (Admin / Staff Dashboard)         │
└───────────────┬──────────────────────────┘
                │ HTTP Requests (JSON)
                ▼
┌──────────────────────────────────────────┐
│          FastAPI Router Layer            │
│  (Input Validation using Pydantic DTOs)  │
└───────────────┬──────────────────────────┘
                ▼
┌──────────────────────────────────────────┐
│      Middleware / Auth Layer             │
│   (RBAC: Admin vs. Staff checks)         │
└───────────────┬──────────────────────────┘
                ▼
┌──────────────────────────────────────────┐
│             Service Layer                │
│    (Business Logic & Validation)         │
└───────────────┬──────────────────────────┘
                ▼
┌──────────────────────────────────────────┐
│            Repository Layer              │
│  (SQLAlchemy / Soft-Delete Filters)      │
└───────────────┬──────────────────────────┘
                ▼
┌──────────────────────────────────────────┐
│               PostgreSQL                 │
│         (Relational Data Store)          │
└──────────────────────────────────────────┘
```

This structure enforces a clear separation of concerns so that business logic, data access, and API handling remain independent.

---

# 2. Component Responsibilities

## Router Layer
Handles incoming requests from the frontend and maps them to the appropriate service operations.

Responsibilities:
- Accept incoming API requests
- Validate request structure
- Delegate work to the service layer
- Return standardized responses

Routers do not contain business logic.

---

## Service Layer
Contains the core business rules of the system.

Responsibilities:
- Enforce validation rules
- Apply business constraints
- Coordinate student enrollment logic
- Interact with repositories for data operations

---

## Repository Layer
Responsible for interacting with the database.

Responsibilities:
- Retrieve data
- Insert new records
- Update existing records
- Maintain persistence logic

---

## Database Layer
Stores system data including:
- Students
- Courses
- Enrollments

Ensures structural integrity through constraints and relationships.

---

# 3. Request Flow

Example: Assign Course to Student

Step 1 — Frontend  
An admin or staff user submits a request to assign a course.

Step 2 — Router Layer  
The router receives the request and validates the request structure.

Step 3 — Service Layer  
Business rules are checked:
- Student exists
- Course exists
- Enrollment is not duplicated

Step 4 — Repository Layer  
If validation succeeds, the repository writes the enrollment record.

Step 5 — Database  
The enrollment record is stored.

Step 6 — Response  
The result flows back through repository → service → router → frontend.

---

# 4. Dependency Map

```
Frontend
   ↓
Router Layer
   ↓
Service Layer
   ↓
Repository Layer
   ↓
Database
```

Rule: higher layers depend on lower layers only.

---

# 5. Architectural Decisions (ADR)

## ADR‑01: Layered Architecture

Context: The system requires clear separation between request handling, business logic, and data access.

Decision: Implement a layered architecture (Router → Service → Repository → Database).

Rationale: Improves maintainability, testability, and separation of concerns.

Consequences: Adds an extra abstraction layer but greatly improves system clarity.

---

## ADR‑02: Soft Deletion Strategy

Context: Removing student records could break historical enrollment data.

Decision: Implement soft deletion where students are marked inactive rather than removed.

Rationale: Preserves historical data and prevents broken relationships.

Consequences: Queries must filter inactive records.

---

## ADR‑03: Role‑Based Access Control

Context: Admin and staff require different system permissions.

Decision: Implement role‑based access restrictions for system operations.

Rationale: Prevents unauthorized data modification and protects system integrity.

Consequences: All protected operations must validate user roles.

---

# 6. Future Extensibility (10x Scale)

If system usage grows significantly, the architecture can evolve with:

### Database Scaling
- Read replicas for heavy read workloads
- Improved indexing strategies

### Service Expansion
- Splitting services into independent modules

### Caching
- Cache frequently accessed data (student lists, course catalogs)

### Infrastructure Scaling
- Deploy backend behind load balancers
- Horizontal scaling using containers

### Multi‑Tenant Capability
If future requirements demand multiple institutions, the data model must introduce tenant isolation.
