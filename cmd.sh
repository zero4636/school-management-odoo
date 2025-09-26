./odoo-bin -u school_core -d odoo
./odoo-bin -u school_core -d odoo --without-demo=none

./odoo-bin -d odoo -u school_portal --stop-after-init

./odoo-bin -d odoo -i school_portal --stop-after-init

odoo-bin -d your_database -i school_core --load=web

# Nếu module đã cài rồi, chỉ update
odoo-bin -d your_se -u school_core --load=web

./odoo-bin -d odoo --logfile=/odoo/var/log/odoo.log --log-level=info (chỉ thực thi lúc đấy thôi)
./odoo-bin -c /odoo/debian/odoo.conf -d odoo --logfile=/odoo/var/log/odoo.log --log-level=debug --dev=all (cái này mới ghi lại config)

./odoo-bin shell -d odoo (cmd odoo)


./odoo-bin -c debian/odoo.conf -d odoo -i school_portal --stop-after-init (install)
./odoo-bin -c debian/odoo.conf -d odoo -u school_portal --stop-after-init (update)


