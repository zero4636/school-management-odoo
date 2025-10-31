from odoo import models, api

class SchoolStudentAPI(models.Model):
    _inherit = "school.student"

    @api.model
    def api_list_students(self, page=1, per_page=20, domain=None, fields=None):
        """
        List students with pagination support.
        
        Args:
            page (int): Page number (default: 1, min: 1)
            per_page (int): Results per page (default: 20, min: 1, max: 100)
            domain (list): Optional search domain filter
            fields (list): Fields to return in response
            
        Returns:
            dict: {
                'total': int,
                'page': int,
                'per_page': int,
                'students': list of student records
            }
        """
        if not page or page < 1:
            page = 1
        if not per_page or per_page < 1:
            per_page = 20
        if per_page > 100:
            per_page = 100

        domain = domain or []
        fields = fields or ["id", "name", "student_id", "dob", "gender", "age", "active", "user_id"]
        offset = (page - 1) * per_page
        total = self.search_count(domain)
        records = self.search_read(domain, fields, offset=offset, limit=per_page)

        for rec in records:
            if isinstance(rec.get("user_id"), (list, tuple)):
                rec["user_id"] = {"id": rec["user_id"][0], "name": rec["user_id"][1]}
        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "students": records,
        }
