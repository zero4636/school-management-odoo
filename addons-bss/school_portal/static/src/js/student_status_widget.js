import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.StudentStatusWidgetInit = publicWidget.Widget.extend({
    selector: '#student_status_widget',
    start() {
        const $el = this.$el;
        const active = $el.data('active');
        const studentId = $el.data('student-id');

        const html = `
            <span class="badge ${active ? 'bg-success' : 'bg-secondary'}">
                ${active ? 'Active' : 'Inactive'}
            </span>
            <button class="btn btn-sm btn-info ms-2" id="show_student_popup">More Info</button>
        `;
        $el.html(html);

        $el.find('#show_student_popup').on('click', () => {
            alert(`Student info popup!\nID: ${studentId}`);
        });
    },
});
