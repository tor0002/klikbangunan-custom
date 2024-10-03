# -*- coding: utf-8 -*-
{
    'name': "KSI Inventory Adjustment for KlikBangunan",

    'summary': """
        KSI Inventory Adjustment for
        Klik Bangunan""",

    'description': """
        KSI Inventory Adjustment for Klik Bangunan
    """,

    'author': "Pt. Ismata Nusantara Abadi",
    'website': "https://www.ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product', 'stock', 'sale_stock', 'purchase_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        
        'views/custom_adjustment_view.xml',
        'views/stock_move_line_view.xml',
        'views/stock_quant_view.xml',
        
        'wizard/stock_inventory_adjustment_view.xml',
    ],
    
    'application': True
}
