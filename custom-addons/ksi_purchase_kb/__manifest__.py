# -*- coding: utf-8 -*-
{
    'name': "KSI Purchase for KlikBangunan",

    'summary': """
        KSI Purchase for
        Klik Bangunan""",

    'description': """
        KSI Purchase for Klik Bangunan
    """,

    'author': "Pt. Ismata Nusantara Abadi",
    'website': "https://www.ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase','purchase_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_view.xml',
        'report/purchase_quotation_templates.xml',
        'report/purchase_order_templates.xml',
    ],
    
    'application': True
}
