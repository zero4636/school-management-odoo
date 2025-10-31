from odoo import models, api
from odoo.exceptions import ValidationError

class SchoolEnrollmentAPI(models.Model):
    _inherit = "school.enrollment"

    @api.model
    def api_list_enrollments(self, student_identifier, page=1, per_page=20):
        """
        List enrollments for a specific student with pagination.
        
        Args:
            student_identifier (int or str): Student ID (numeric) or student_id (string code)
            page (int): Page number (default: 1, min: 1)
            per_page (int): Results per page (default: 20, min: 1, max: 100)
            
        Returns:
            dict: {
                'total': int,
                'page': int,
                'per_page': int,
                'student': dict with student info,
                'enrollments': list of enrollment records
            }
            
        Raises:
            ValidationError: If student not found
        """
        Student = self.env["school.student"]

        if isinstance(student_identifier, int):
            student = Student.search([("id", "=", student_identifier)], limit=1)
        else:
            student = Student.search([("student_id", "=", student_identifier)], limit=1)
        if not student:
            raise ValidationError(f"Student '{student_identifier}' not found")

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 20
        if per_page > 100:
            per_page = 100

        domain = [("student_id", "=", student.id)]
        offset = (page - 1) * per_page
        total = self.search_count(domain)

        enrollments = self.search_read(
            domain,
            ["id", "student_id", "subject_id", "state", "enrollment_date"],
            offset=offset,
            limit=per_page,
        )

        for e in enrollments:
            student_ref = e.pop("student_id", None)
            subject_ref = e.pop("subject_id", None)
            if isinstance(student_ref, (list, tuple)):
                e["student"] = {"id": student_ref[0], "name": student_ref[1]}
            if isinstance(subject_ref, (list, tuple)):
                e["subject"] = {"id": subject_ref[0], "name": subject_ref[1]}

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "student": {
                "id": student.id,
                "name": student.name,
                "student_id": student.student_id,
            },
            "enrollments": enrollments,
        }

    @api.model
    def api_add_enrollment(self, student_identifier, subject_identifier):
        """
        Add a new enrollment (enroll a student in a subject).
        
        Args:
            student_identifier (int or str): Student ID (numeric) or student_id (string code)
            subject_identifier (int or str): Subject ID (numeric) or subject name (string)
            
        Returns:
            dict: {
                'status': 'success' or 'error',
                'message': str,
                'enrollment_id': int (only on success)
            }
        """
        Student = self.env["school.student"]
        Subject = self.env["school.subject"]

        if isinstance(student_identifier, int):
            student = Student.search([("id", "=", student_identifier)], limit=1)
        else:
            student = Student.search([("student_id", "=", student_identifier)], limit=1)
        if not student:
            return {"status": "error", "message": f"Student '{student_identifier}' not found"}

        if isinstance(subject_identifier, int):
            subject = Subject.search([("id", "=", subject_identifier)], limit=1)
        else:
            subject = Subject.search([("name", "=", subject_identifier)], limit=1)
        if not subject:
            return {"status": "error", "message": f"Subject '{subject_identifier}' not found"}

        exists = self.search([
            ("student_id", "=", student.id),
            ("subject_id", "=", subject.id)
        ], limit=1)

        if exists:
            return {
                "status": "error",
                "message": f"Student '{student.name}' is already enrolled in subject '{subject.name}'"
            }

        enrollment = self.create({
            "student_id": student.id,
            "subject_id": subject.id,
            "state": "active",
        })

        return {
            "status": "success",
            "message": f"{student.name} enrolled in {subject.name}",
            "enrollment_id": enrollment.id
        }