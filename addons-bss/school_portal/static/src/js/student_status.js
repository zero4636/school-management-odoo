odoo.define('school_portal.StudentStatusWidget', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.StudentStatusWidget = publicWidget.Widget.extend({
        selector: '#student_status_widget',
        start: function () {
            var active = this.$el.data('active') === 'true';
            this.$el.text(active ? "Status: Active" : "Status: Inactive");
            return this._super.apply(this, arguments);
        }
    });
});
