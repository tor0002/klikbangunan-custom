# -*- coding: utf-8 -*-
{
    'name': "custom_ksi_delivery",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock_picking_batch', 'stock', 'product'],

    # always loaded
    'data': [
        'views/ksi_drivers_views.xml',
        'views/stock_picking_batch_views.xml',
        'views/stock_move_line_view.xml',
        'views/product_template_views.xml',
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
