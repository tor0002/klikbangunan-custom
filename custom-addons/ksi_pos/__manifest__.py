# -*- coding: utf-8 -*-
{
    'name': "ksi_pos",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','point_of_sale','ksi_partner_kb','ksi_stock_kb', 'pos_coupon', 'coupon', 'sh_pos_order_sync','pos_hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        
        'views/coupon_rule.xml',
        'views/pos_db.xml',
        'views/pos_sess.xml',
        
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'ksi_pos/static/src/css/ksi-custom.css',
            'ksi_pos/static/src/js/display_stock.css',
            # 'pos_access_right/static/src/js/models.js',
            'ksi_pos/static/src/js/ClosePosPopup.js',
            # 'ksi_pos/static/src/js/Coupon.js',
            # 'pos_access_right/static/src/js/NumpadWidget.js',
            # 'pos_access_right/static/src/js/TicketScreen.js',
        ],
        'web.assets_qweb': [
            'ksi_pos/static/src/xml/**/*',
            'ksi_pos/static/src/xml/*',
            'ksi_pos/static/src/xml/*.xml',
        ],
    }
}
