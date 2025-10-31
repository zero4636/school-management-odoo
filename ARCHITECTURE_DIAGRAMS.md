# School Management API - Architecture Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     External Applications                    │
│  (Mobile App, Web Portal, Third-party Systems, etc.)        │
└────────────────────────┬────────────────────────────────────┘
                         │ XML-RPC / HTTP
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Odoo Server                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Authentication Layer                      │  │
│  │  /xmlrpc/2/common - authenticate(db, user, pass)     │  │
│  └───────────────────┬───────────────────────────────────┘  │
│                      │ Returns UID                           │
│                      ▼                                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              API Execution Layer                       │  │
│  │  /xmlrpc/2/object - execute_kw(db, uid, pass, ...)   │  │
│  └───────────────────┬───────────────────────────────────┘  │
│                      │                                        │
│                      ▼                                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              School API Module (school_api)           │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  SchoolStudentAPI                              │  │  │
│  │  │  - api_list_students()                          │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  SchoolEnrollmentAPI                           │  │  │
│  │  │  - api_list_enrollments()                       │  │  │
│  │  │  - api_add_enrollment()                         │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────┬───────────────────────────────────┘  │
│                      │                                        │
│                      ▼                                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           School Core Module (school_core)            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────┐           │  │
│  │  │ Student  │  │ Subject  │  │ Teacher   │           │  │
│  │  │  Model   │  │  Model   │  │  Model    │           │  │
│  │  └──────────┘  └──────────┘  └───────────┘           │  │
│  │  ┌───────────────────────────────────────┐            │  │
│  │  │      Enrollment Model                 │            │  │
│  │  └───────────────────────────────────────┘            │  │
│  └───────────────────┬───────────────────────────────────┘  │
│                      │ Odoo ORM                              │
│                      ▼                                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              PostgreSQL Database                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## API Flow Diagrams

### 1. List Students API Flow

```
Client                  Odoo Server              school_api           school_core
  │                          │                        │                     │
  │  1. Authenticate         │                        │                     │
  ├─────────────────────────>│                        │                     │
  │                          │                        │                     │
  │  2. Return UID           │                        │                     │
  │<─────────────────────────┤                        │                     │
  │                          │                        │                     │
  │  3. execute_kw(          │                        │                     │
  │     'school.student',    │                        │                     │
  │     'api_list_students', │                        │                     │
  │     [page, per_page])    │                        │                     │
  ├─────────────────────────>│                        │                     │
  │                          │                        │                     │
  │                          │  4. Call method        │                     │
  │                          ├───────────────────────>│                     │
  │                          │                        │                     │
  │                          │                        │  5. Validate params │
  │                          │                        │─┐                   │
  │                          │                        │ │                   │
  │                          │                        │<┘                   │
  │                          │                        │                     │
  │                          │                        │  6. Search students │
  │                          │                        ├────────────────────>│
  │                          │                        │                     │
  │                          │                        │  7. Return records  │
  │                          │                        │<────────────────────┤
  │                          │                        │                     │
  │                          │                        │  8. Transform data  │
  │                          │                        │─┐                   │
  │                          │                        │ │                   │
  │                          │                        │<┘                   │
  │                          │                        │                     │
  │                          │  9. Return response    │                     │
  │                          │<───────────────────────┤                     │
  │                          │                        │                     │
  │  10. JSON Response       │                        │                     │
  │<─────────────────────────┤                        │                     │
  │                          │                        │                     │
```

### 2. Add Enrollment API Flow

```
Client                  Odoo Server              school_api           school_core
  │                          │                        │                     │
  │  1. execute_kw(          │                        │                     │
  │     'school.enrollment', │                        │                     │
  │     'api_add_enrollment',│                        │                     │
  │     [student_id,         │                        │                     │
  │      subject_id])        │                        │                     │
  ├─────────────────────────>│                        │                     │
  │                          │                        │                     │
  │                          │  2. Call method        │                     │
  │                          ├───────────────────────>│                     │
  │                          │                        │                     │
  │                          │                        │  3. Find student    │
  │                          │                        ├────────────────────>│
  │                          │                        │                     │
  │                          │                        │  4. Student found   │
  │                          │                        │<────────────────────┤
  │                          │                        │                     │
  │                          │                        │  5. Find subject    │
  │                          │                        ├────────────────────>│
  │                          │                        │                     │
  │                          │                        │  6. Subject found   │
  │                          │                        │<────────────────────┤
  │                          │                        │                     │
  │                          │                        │  7. Check existing  │
  │                          │                        ├────────────────────>│
  │                          │                        │                     │
  │                          │                        │  8. Not exists      │
  │                          │                        │<────────────────────┤
  │                          │                        │                     │
  │                          │                        │  9. Create enrollment│
  │                          │                        │     (state='active')│
  │                          │                        ├────────────────────>│
  │                          │                        │                     │
  │                          │                        │  10. Created        │
  │                          │                        │<────────────────────┤
  │                          │                        │                     │
  │                          │  11. Return success    │                     │
  │                          │<───────────────────────┤                     │
  │                          │                        │                     │
  │  12. Success Response    │                        │                     │
  │<─────────────────────────┤                        │                     │
  │  {status: "success",     │                        │                     │
  │   enrollment_id: 123}    │                        │                     │
  │                          │                        │                     │
```

## Data Model Relationships

```
┌─────────────────┐
│   res.users     │
│  (Odoo Users)   │
└────┬────────┬───┘
     │        │
     │        │ inherits
     │        │
     │   ┌────▼────────────┐
     │   │ school.teacher  │
     │   │ - employee_code │
     │   └────┬────────────┘
     │        │
     │        │ teaches
     │        │
     │   ┌────▼────────┐
     │   │   subject   │◄────┐
     │   │   - name    │     │
     │   │   - credit  │     │
     │   └─────────────┘     │
     │                       │
     │ links to              │ enrolled in
     │                       │
┌────▼──────────┐      ┌─────┴───────────┐
│ school.student│      │ school.enrollment│
│ - name        │◄─────│ - student_id    │
│ - student_id  │      │ - subject_id    │
│ - dob         │      │ - state         │
│ - gender      │      │ - enroll_date   │
│ - age         │      └─────────────────┘
└───────────────┘
```

## API Response Formats

### List Students Response
```json
{
  "total": 150,
  "page": 1,
  "per_page": 20,
  "students": [
    {
      "id": 1,
      "name": "John Doe",
      "student_id": "STU001",
      "dob": "2000-01-15",
      "gender": "male",
      "age": 25,
      "active": true,
      "user_id": {
        "id": 5,
        "name": "John Doe"
      }
    }
  ]
}
```

### List Enrollments Response
```json
{
  "total": 5,
  "page": 1,
  "per_page": 20,
  "student": {
    "id": 1,
    "name": "John Doe",
    "student_id": "STU001"
  },
  "enrollments": [
    {
      "id": 10,
      "student": {
        "id": 1,
        "name": "John Doe"
      },
      "subject": {
        "id": 1,
        "name": "Mathematics"
      },
      "state": "active",
      "enrollment_date": "2025-10-01"
    }
  ]
}
```

### Add Enrollment Response (Success)
```json
{
  "status": "success",
  "message": "John Doe enrolled in Mathematics",
  "enrollment_id": 10
}
```

### Add Enrollment Response (Error)
```json
{
  "status": "error",
  "message": "Student 'STU999' not found"
}
```

## Security Flow

```
┌────────────┐
│   Client   │
└─────┬──────┘
      │
      │ 1. Send credentials
      ▼
┌──────────────────┐
│  Authentication  │
│      Layer       │
└─────┬────────────┘
      │ 2. Validate & return UID
      ▼
┌──────────────────┐
│   Access Control │ ◄──── Check user groups
│      Check       │ ◄──── Check record rules
└─────┬────────────┘
      │ 3. Authorized
      ▼
┌──────────────────┐
│   API Method     │
│   Execution      │
└─────┬────────────┘
      │ 4. Execute with ORM
      ▼
┌──────────────────┐
│    Database      │ ◄──── No direct SQL
│    (via ORM)     │ ◄──── SQL injection safe
└──────────────────┘
```

## Usage Example Flow

```python
# 1. Setup connection
import xmlrpc.client
url = "http://127.0.0.1:8069"
db = "odoo"
username = "user@example.com"
password = "password"

# 2. Authenticate
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

# 3. Connect to models
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# 4. List students
students = models.execute_kw(
    db, uid, password,
    'school.student', 'api_list_students',
    [1, 20]  # page=1, per_page=20
)

# 5. Get enrollments
enrollments = models.execute_kw(
    db, uid, password,
    'school.enrollment', 'api_list_enrollments',
    [students['students'][0]['id'], 1, 20]
)

# 6. Add enrollment
result = models.execute_kw(
    db, uid, password,
    'school.enrollment', 'api_add_enrollment',
    [1, 5]  # student_id=1, subject_id=5
)
```

## Performance Considerations

```
Request Limits:
├── per_page: max 100 records
├── Pagination: Required for large datasets
└── Database Indexing:
    ├── student.student_id (indexed)
    └── teacher.employee_code (indexed)

Caching Strategy (Future):
├── Static data: subjects, teachers
├── Cache duration: 5-15 minutes
└── Invalidation: On updates

Query Optimization:
├── Use search_read (single query)
├── Limit fields in response
└── Add database indices as needed
```
