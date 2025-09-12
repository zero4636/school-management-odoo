odoo.define('school_portal.StudentStatusWidget', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');

    var StudentStatusWidget = Widget.extend({
        template: 'school_portal.student_status',
        init: function (parent, options) {
            this._super(parent);
            this.student = options.student || {active: true};
        },
        start: function () {
            if (this.student.active) {
                this.$el.text("Status: Active");
            } else {
                this.$el.text("Status: Inactive");
            }
        },
    });

    // Attach vào div id="student_status_widget"
    publicWidget.registry.StudentStatusWidget = publicWidget.Widget.extend({
        selector: '#student_status_widget',
        start: function () {
            var widget = new StudentStatusWidget(this, {student: {active: true}});
            widget.appendTo(this.$el);
            return this._super.apply(this, arguments);
        }
    });

    return StudentStatusWidget;
});
