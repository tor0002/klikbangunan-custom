# -*- coding: utf-8 -*-
{
    'name': "KSI Partner for KlikBangunan",

    'summary': """
        KSI Partner for
        Klik Bangunan""",

    'description': """
        KSI Partner for Klik Bangunan
    """,

    'author': "Pt. Ismata Nusantara Abadi",
    'website': "https://www.ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale','point_of_sale','pos_loyalty','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        
        # 'static/src/xml/Loyalty.xml',
        
        # 'views/sequence_data.xml',
        
        'views/res_partner_view.xml',
        'views/res_model_view.xml',
        'views/registration_outlet_view.xml',
        'views/media_acquisition_view.xml',
        'views/member_type_view.xml',
    ],
    
    'assets': {
        'web.assets_qweb': [
            'ksi_partner_kb/static/src/xml/**/*',
            'ksi_partner_kb/static/src/xml/*',
            'ksi_partner_kb/static/src/xml/*.xml',
        ],
        'point_of_sale.assets': [
            'ksi_partner_kb/static/src/js/**',
            'ksi_partner_kb/static/src/js/*',
            'ksi_partner_kb/static/src/js/models.js',
            'ksi_partner_kb/static/src/js/PaymentScreenCustom.js',
            
        ],
    },
    
    'application': True
}
