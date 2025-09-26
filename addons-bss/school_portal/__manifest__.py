{
    "name": "School Portal",
    "summary": "Portal for Students and Teachers",
    "version": "1.0",
    "depends": ["base", "portal", "website", "school_core"],
    "author": "Dong TD",
    "website": "https://odoo.test",
    "category": "Education",
    "data": [
        "views/portal_templates.xml",
        "views/portal_student.xml",
        "views/portal_teacher.xml",
        "views/legacy_widget_templates.xml",
        "views/owl_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "school_portal/static/src/js/student_status.js",
            "school_portal/static/src/scss/portal.scss",
        ],
        "web.assets_qweb": [
            "school_portal/static/src/xml/*.xml",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
