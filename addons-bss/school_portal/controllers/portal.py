from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request

class SchoolPortal(CustomerPortal):
    _items_per_page = 10


    def _get_student_searchbar_sortings(self):
        return {
            'name': {'label': _('Name'), 'order': 'name asc'},
            'student_id': {'label': _('Student ID'), 'order': 'student_id asc'},
            'dob': {'label': _('Date of Birth'), 'order': 'dob desc'},
            'age': {'label': _('Age'), 'order': 'age desc'},
            'create_date': {'label': _('Created On'), 'order': 'create_date desc'},
        }

    def _get_student_searchbar_filters(self):
        return {
            'all': {'label': _('All'), 'domain': []},
            'male': {'label': _('Male'), 'domain': [('gender', '=', 'male')]},
            'female': {'label': _('Female'), 'domain': [('gender', '=', 'female')]},
            'other': {'label': _('Other'), 'domain': [('gender', '=', 'other')]},
            'active': {'label': _('Active'), 'domain': [('active', '=', True)]},
            'inactive': {'label': _('Inactive'), 'domain': [('active', '=', False)]},
            'minor': {'label': _('Under 18'), 'domain': [('age', '<', 18)]},
            'adult': {'label': _('18 and above'), 'domain': [('age', '>=', 18)]},
        }

    def _get_teacher_searchbar_sortings(self):
        return {
            'name': {'label': _('Name'), 'order': 'name asc'},
            'employee_code': {'label': _('Employee Code'), 'order': 'employee_code asc'}
        }

    def _get_teacher_searchbar_filters(self):
        return {
            'all': {'label': _('All'), 'domain': []},
        }

    @http.route(['/my/students', '/my/students/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_students(self, page=1, sortby='name', filterby='all', search=None, search_in='all', **kw):
        values = self._prepare_portal_layout_values()
        Student = request.env['school.student']

        # Searchbar options
        searchbar_sortings = self._get_student_searchbar_sortings()
        searchbar_filters = self._get_student_searchbar_filters()
        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
            'name': {'input': 'name', 'label': _('Name')},
            'student_id': {'input': 'student_id', 'label': _('Student ID')},
        }

        if sortby not in searchbar_sortings:
            sortby = 'student_id'
        sort_order = searchbar_sortings[sortby]['order']

        if filterby not in searchbar_filters:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        if search:
            search_domain = []
            if search_in in ('all', 'name'):
                search_domain = ['|', ('name', 'ilike', search), ('student_id', 'ilike', search)]
            elif search_in == 'student_id':
                search_domain = [('student_id', 'ilike', search)]
            domain += search_domain

        student_count = Student.search_count(domain)

        pager = portal_pager(
            url="/my/students",
            total=student_count,
            page=page,
            step=self._items_per_page,
            url_args={'sortby': sortby, 'filterby': filterby, 'search_in': search_in, 'search': search},
        )
        students = Student.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'students': students,
            'page_name': 'students',
            'pager': pager,
            'default_url': '/my/students',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
        })
        return request.render("school_portal.portal_student_page", values)

    @http.route(['/my/students/<int:student_id>'], type='http', auth='public', website=True)
    def portal_student_detail(self, student_id, **kw):
        student = request.env['school.student'].sudo().browse(student_id)
        return request.render("school_portal.portal_student_detail_page", {'student': student, 'page_name': 'student'})

    @http.route(['/my/teachers', '/my/teachers/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_teachers(self, page=1, sortby='name', filterby='all', search=None, search_in='all', **kw):
        values = self._prepare_portal_layout_values()
        Teacher = request.env['school.teacher'].sudo()

        searchbar_sortings = self._get_teacher_searchbar_sortings()
        searchbar_filters = self._get_teacher_searchbar_filters()
        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
            'name': {'input': 'name', 'label': _('Name')},
            'employee_code': {'input': 'employee_code', 'label': _('Employee Code')},
        }

        if sortby not in searchbar_sortings:
            sortby = 'employee_code'
        sort_order = searchbar_sortings[sortby]['order']

        if filterby not in searchbar_filters:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        if search:
            search_domain = []
            if search_in in ('all', 'name'):
                search_domain = ['|', ('name', 'ilike', search), ('employee_code', 'ilike', search)]
            elif search_in == 'employee_code':
                search_domain = [('employee_code', 'ilike', search)]
            domain += search_domain

        teacher_count = Teacher.search_count(domain)
        pager = portal_pager(
            url='/my/teachers',
            total=teacher_count,
            page=page,
            step=self._items_per_page,
            url_args={'sortby': sortby, 'filterby': filterby, 'search_in': search_in, 'search': search},
        )

        teachers = Teacher.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'teachers': teachers,
            'page_name': 'teachers',
            'pager': pager,
            'default_url': '/my/teachers',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
        })
        return request.render("school_portal.portal_teacher_page", values)

    @http.route(['/my/teachers/<int:teacher_id>'], type='http', auth='user', website=True)
    def portal_teacher_detail(self, teacher_id, **kw):
        teacher = request.env['school.teacher'].sudo().browse(teacher_id)
        subjects_info = []
        for subject in teacher.subject_ids:
            students = subject.enrollment_ids.mapped('student_id')
            subjects_info.append({
                'subject': subject,
                'students': students,
            })

        values = {
            'teacher': teacher,
            'page_name': 'teacher',
            'subjects_info': subjects_info,
        }
        return request.render("school_portal.portal_teacher_detail_page", values)


