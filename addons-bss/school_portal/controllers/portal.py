from odoo import http
from odoo.http import request

class SchoolPortal(http.Controller):

    @http.route(['/my/student'], type='http', auth='public', website=True)
    def portal_student(self, **kw):
        student = request.env['school.student'].sudo().search([])
        return request.render("school_portal.portal_student_page", {"students": student})

    @http.route(['/my/teacher'], type='http', auth='public', website=True)
    def portal_teacher(self, **kw):
        teacher = request.env['school.teacher'].sudo().search([])
        return request.render("school_portal.portal_teacher_page", {"teachers": teacher})
