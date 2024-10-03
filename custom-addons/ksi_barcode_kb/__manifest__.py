# -*- coding: utf-8 -*-
{
    'name': "ksi_barcode_kb",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
        testing
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','product_multiple_barcodes','stock_barcode'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report_barcode_ksi.xml',
        'report/ksi_barcode_layout.xml',
        'report/product_product_templates.xml',
        'views/stock_picking_view.xml',
        'wizard/product_label_layout_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'product.assets': [
            # 'ksi_barcode_kb/static/src/css/ksi_custom_barcode.css',
            # 'ksi_barcode_kb/static/src/scss/ksi_custom_barcode.scss',
            # 'pos_access_right/static/src/js/models.js',
            # 'ksi_pos/static/src/js/ClosePosPopup.js',
            # 'pos_access_right/static/src/js/NumpadWidget.js',
            # 'pos_access_right/static/src/js/TicketScreen.js',
        ],
        'web.assets_qweb': [
            # 'ksi_pos/static/src/xml/**/*',
            # 'ksi_pos/static/src/xml/*',
            # 'ksi_pos/static/src/xml/*.xml',
        ],
         'web.report_assets_common': [
            'ksi_barcode_kb/static/src/scss/ksi_custom_barcode.scss',
            # 'ksi_barcode_kb/static/src/css/ksi_custom_barcode.css',
        ],
    }
}
