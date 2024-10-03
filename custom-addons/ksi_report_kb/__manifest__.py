# -*- coding: utf-8 -*-
{
    'name': "KSI Report for KlikBangunan",

    'summary': """
        KSI REPORT KB
        Custom module of reporting for KlikBangunan""",

    'description': """
        KSI REPORT KB - a custom module of reporting for KlikBangunan
    """,

    'author': "Pt. Ismata Nusantara Abadi",
    'website': "https://ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'report_xlsx', 'mail', 'stock', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/ksi_report_kb_security.xml',
        
        'report/report_action.xml',
        
        'views/menu_item_view.xml',
        'views/sale_and_margin_view.xml',
        'views/sale_transaction_view.xml',
        
        'views/res_config_settings_view.xml',
        
        # 'views/templates.xml',
        # 'views/views.xml',
        
        'wizard/target_vs_sales_wizard.xml',
        'wizard/sale_transaction_wizard_view.xml',
    ],
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    # 'assets': {
    #     'web.assets': [
    #         'ksi_report_kb/static/src/js/list_renderer.js',
    #     ],
        # 'point_of_sale.assets': [
        #     'ksi_report_kb/static/src/js/action_handler.js',
        # ],
    #     'web.assets_qweb': [
    #         'ksi_report_kb/static/src/xml/**/*',
    #         'ksi_report_kb/static/src/xml/*',
    #         'ksi_report_kb/static/src/xml/*.xml',
    #     ],
    # }
}