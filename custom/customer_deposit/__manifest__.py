# -*- coding: utf-8 -*-

{
    'name': 'Customer Deposit',
    'category': 'Hidden',
    'summary': 'Customer Deposit',
    'description': "",
    'depends': ['base','account','point_of_sale','base_automation'],
    'Author':'Boyke Budi Pratama',
    'data': [
        'data/base_automation.xml',
        'views/res_partner.xml',
        'views/account_payment_view.xml',
        'views/pos_payment_method_views.xml',
        'views/point_of_sale_template.xml',
    ],
    'qweb': ['static/src/xml/deposit.xml'],
    'installable': True,
}
