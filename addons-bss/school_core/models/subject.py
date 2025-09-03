from odoo import models, fields

class Subject(models.Model):
    _name = "school.subject"
    _description = "Subject"

    name = fields.Char("Subject Name", required=True)
    credit = fields.Integer("Credit", default=3)
    teacher_id = fields.Many2one("school.teacher", string="Teacher")
    enrollment_ids = fields.One2many("school.enrollment", "subject_id", string="Enrollments")
