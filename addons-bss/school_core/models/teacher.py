from odoo import models, fields, api
from odoo.exceptions import UserError

class Teacher(models.Model):
    _name = "school.teacher"
    _description = "Teacher"

    name = fields.Char("Name", required=True)
    employee_code = fields.Char("Employee Code", required=True, copy=False, index=True)
    user_id = fields.Many2one("res.users", string="User Account")
    subject_ids = fields.One2many("school.subject", "teacher_id", string="Subjects")

    _sql_constraints = [
        ('unique_employee_code', 'unique(employee_code)', 'Employee Code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if not vals.get('employee_code') or vals.get('employee_code') == 'New':
            seq = self.env['ir.sequence'].next_by_code('school.teacher')
            if not seq:
                raise UserError("The 'school.teacher' sequence is not configured properly!")
            vals['employee_code'] = seq
        return super(Teacher, self).create(vals)