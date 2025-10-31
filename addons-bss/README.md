# School Management System - API Documentation

This directory contains the School Management System modules for Odoo.

## Quick Links

- **[SCHOOL_API_SUMMARY.md](../SCHOOL_API_SUMMARY.md)** - Complete API documentation and summary
- **[IMPLEMENTATION_NOTES.md](../IMPLEMENTATION_NOTES.md)** - Implementation details (Vietnamese & English)
- **[ARCHITECTURE_DIAGRAMS.md](../ARCHITECTURE_DIAGRAMS.md)** - Architecture diagrams and flows
- **[test_school_api.py](../test_school_api.py)** - API usage examples

## Modules

### school_core
Core module containing the base models:
- **Student**: Student information and management
- **Teacher**: Teacher information and account management  
- **Subject**: Course/subject management
- **Enrollment**: Student-subject enrollment tracking

### school_api
API extension module providing XML-RPC endpoints:
- `api_list_students`: List students with pagination
- `api_list_enrollments`: List enrollments for a student
- `api_add_enrollment`: Enroll a student in a subject

### school_portal
Portal module for student and teacher web access

## Getting Started

1. Install the modules:
   ```bash
   # Install school_core first
   # Then install school_api
   ```

2. Test the API:
   ```bash
   python3 test_school_api.py
   ```

3. Read the documentation:
   - Start with SCHOOL_API_SUMMARY.md for complete overview
   - Check ARCHITECTURE_DIAGRAMS.md for visual understanding
   - Read IMPLEMENTATION_NOTES.md for detailed logic explanation

## API Usage

See [test_school_api.py](../test_school_api.py) for complete examples.

### Basic Authentication
```python
import xmlrpc.client

url = "http://127.0.0.1:8069"
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
```

### List Students
```python
students = models.execute_kw(db, uid, password,
    'school.student', 'api_list_students', [1, 20])
```

### List Enrollments
```python
enrollments = models.execute_kw(db, uid, password,
    'school.enrollment', 'api_list_enrollments', [student_id, 1, 20])
```

### Add Enrollment
```python
result = models.execute_kw(db, uid, password,
    'school.enrollment', 'api_add_enrollment', [student_id, subject_id])
```

## Documentation Structure

```
.
├── SCHOOL_API_SUMMARY.md          # Complete API reference
├── IMPLEMENTATION_NOTES.md        # Implementation details (Vietnamese/English)
├── ARCHITECTURE_DIAGRAMS.md       # Visual architecture documentation
├── test_school_api.py             # Working examples
└── addons-bss/
    ├── school_core/               # Core models
    │   ├── models/
    │   │   ├── student.py
    │   │   ├── teacher.py
    │   │   ├── subject.py
    │   │   └── enrollment.py
    │   ├── views/
    │   ├── security/
    │   └── data/
    ├── school_api/                # API extension
    │   └── models/
    │       ├── student_api.py
    │       └── enrollment_api.py
    └── school_portal/             # Web portal
        ├── controllers/
        ├── views/
        └── static/
```

## Recent Changes

- ✅ Added comprehensive API documentation
- ✅ Added docstrings to all API methods
- ✅ Added pagination limits (max 100 per page)
- ✅ Changed enrollment state to 'active' by default
- ✅ Fixed test file comments
- ✅ Created architecture diagrams
- ✅ Created bilingual implementation notes

## Support

For questions or issues:
1. Read the documentation in SCHOOL_API_SUMMARY.md
2. Check the examples in test_school_api.py
3. Review the architecture diagrams
4. Check the implementation notes for detailed explanations

## License

See main repository LICENSE file.
