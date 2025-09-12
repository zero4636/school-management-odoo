from odoo import http
from odoo.http import request

class SchoolPortal(http.Controller):

    @http.route(['/my/student'], type='http', auth="user", website=True)
    def portal_student(self, **kw):
        student = request.env['school.student'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        return request.render("school_portal.portal_student_page", {"student": student})

    @http.route(['/my/teacher'], type='http', auth="user", website=True)
    def portal_teacher(self, **kw):
        teacher = request.env['school.teacher'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        return request.render("school_portal.portal_teacher_page", {"teacher": teacher})
