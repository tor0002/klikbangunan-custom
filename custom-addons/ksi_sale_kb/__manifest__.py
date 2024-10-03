# -*- coding: utf-8 -*-
{
    'name': "KSI Sale for KlikBangunan",

    'summary': """
        KSI Sale for
        Klik Bangunan""",

    'description': """
        KSI Sale for Klik Bangunan
    """,

    'author': "Pt. Ismata Nusantara Abadi",
    'website': "https://www.ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_margin', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_view.xml',
    ],
    
    'application': True
}
