# -*- coding: utf-8 -*-
{
    'name': "KSI Stock for KlikBangunan",

    'summary': """
        KSI Stock for
        Klik Bangunan""",

    'description': """
        KSI Stock for Klik Bangunan
    """,

    'author': "Pt. Ismata Nusantara Abadi",
    'website': "https://www.ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product', 'mail', 'sale_stock', 'purchase_stock','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        
        'data/sequence_data.xml',
        
        'report/report_deliveryslip.xml',
        # 'report/stock_report_view.xml',
        'views/res_config_settings_views.xml',
        'views/product_view.xml',
        'views/product_template_view.xml',
        
        'views/stock_picking_view.xml',
        
        'views/stock_picking_return_views.xml',
        'views/stock_quant_view.xml',
        'views/product_category_views.xml',
        'views/stock_moves_view.xml',
        
        'wizard/stock_backorder_confirmation_view.xml'
    ],
    
    'application': True
}
