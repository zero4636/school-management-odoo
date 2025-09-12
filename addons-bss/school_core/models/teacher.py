from odoo import models, fields, api
from odoo.exceptions import UserError

class Teacher(models.Model):
    _name = "school.teacher"
    _description = "Teacher"
    _inherits = {"res.users": "user_id"}

    user_id = fields.Many2one(
        "res.users",
        string="User Account",
        required=True,
        ondelete="cascade"
    )

    employee_code = fields.Char("Employee Code", required=True, copy=False, index=True)
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

        if not vals.get('user_id'):
            login = vals.get('login')
            password = vals.get('password')
            if not login or not password:
                raise UserError("You must provide login and password when creating a teacher.")

            user = self.env['res.users'].create({
                'name': vals.get('name') or 'Unknown',
                'login': login,
                'password': password,
                'groups_id': [(6, 0, [
                    self.env.ref('school_core.group_school_teacher').id,
                    self.env.ref('base.group_user').id,
                ])]
            })
            vals['user_id'] = user.id

        return super(Teacher, self).create(vals)

