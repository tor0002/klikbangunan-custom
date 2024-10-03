# -*- coding: utf-8 -*-
{
    'name': "ksi_pos_parreto",

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
    'depends': ['base', 'point_of_sale','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/parreto_wizard.xml',
        'views/menuitem_views.xml',
        'views/templates.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'ksi_pos_parreto/static/src/js/tree_button.js',
        ],
        'web.assets_qweb': [
            'ksi_pos_parreto/static/src/xml/tree_button.xml',
        ],
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
