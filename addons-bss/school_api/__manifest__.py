{
    "name": "School API",
    "version": "1.0",
    "summary": "Provide XML-RPC and JSON APIs for School Management System",
    "author": "Dong TD",
    "website": "https://odoo.test",
    "category": "Education",
    "depends": ["school_core", "base"],
    "description": """
    Module mở rộng `school_core`, cung cấp API cho:
    - Danh sách học sinh (phân trang)
    - Danh sách môn học đã đăng ký
    - Thêm học sinh vào môn học
    """,
    "installable": True,
    "application": True,
    "auto_install": False,
}
