import xmlrpc.client

url = "http://127.0.0.1:8069"
db = "odoo"
username = "testmagento321@gmail.com"
password = "Bss123@#"

# 1. Authenticate
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

# 2. Connect to object
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# 3. List students (page 1, 3 per page)
students = models.execute_kw(db, uid, password,
                             'school.student', 'api_list_students',
                             [1, 3])  # page=1, per_page=3
print("Students:", students)
print("==========================================================================")

# 4. List enrollments of a student
student_id = students['students'][0]['id']
enrollments = models.execute_kw(db, uid, password,
                                'school.enrollment', 'api_list_enrollments',
                                [student_id, 1, 20])  # page=1, per_page=20
print("Enrollments:", enrollments)
print("==========================================================================")

# 5. Add student to a subject
res = models.execute_kw(db, uid, password,
                        'school.enrollment', 'api_add_enrollment',
                        [student_id, 'Subject 1'])  # subject_identifier có thể là id hoặc name
print("Add enrollment:", res)
