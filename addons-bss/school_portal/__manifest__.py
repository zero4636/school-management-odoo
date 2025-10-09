{
    "name": "School Portal",
    "summary": "Portal for Students and Teachers",
    "version": "1.0",
    "depends": ["portal", "website", "school_core"],
    "author": "Dong TD",
    "website": "https://odoo.test",
    "category": "Education",
    "data": [
        "views/portal_template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/school_portal/static/src/js/student_status_widget.js",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": True
}
