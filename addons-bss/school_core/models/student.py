from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Student(models.Model):
    _name = "school.student"
    _description = "Student"

    name = fields.Char("Name", required=True)
    student_id = fields.Char("Student ID", required=True, copy=False, index=True)
    dob = fields.Date("Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    user_id = fields.Many2one("res.users", string="User Account")
    enrollment_ids = fields.One2many("school.enrollment", "student_id", string="Enrollments")
    active = fields.Boolean("Active", default=True)

    age = fields.Integer("Age", compute="_compute_age", store=True)

    @api.depends("dob")
    def _compute_age(self):
        for student in self:
            if student.dob:
                today = fields.Date.today()
                student.age = today.year - student.dob.year - ((today.month, today.day) < (student.dob.month, student.dob.day))
            else:
                student.age = 0

    _sql_constraints = [
        ('unique_student_id', 'unique(student_id)', 'Student ID must be unique!')
    ]

    @api.model
    def create(self, vals):
        if not vals.get('student_id'):
            seq = self.env['ir.sequence'].next_by_code('school.student')
            if not seq:
                raise UserError("The 'school.student' sequence is not configured properly!")
            vals['student_id'] = seq
        return super(Student, self).create(vals)
