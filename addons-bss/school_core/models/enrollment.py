from odoo import models, fields, api

class Enrollment(models.Model):
    _name = "school.enrollment"
    _description = "Enrollment"

    student_id = fields.Many2one("school.student", string="Student", required=True)
    subject_id = fields.Many2one("school.subject", string="Subject", required=True)
    enrollment_date = fields.Date("Enrollment Date", default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled')
    ], string="Status", default="draft")

    _sql_constraints = [
        ('unique_enrollment', 'unique(student_id, subject_id)', 'Student is already enrolled in this subject!')
    ]

    @api.constrains("student_id", "subject_id")
    def _check_teacher(self):
        for rec in self:
            if rec.subject_id and rec.student_id:
                pass
