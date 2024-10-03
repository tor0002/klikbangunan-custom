# -*- coding: utf-8 -*-
{
    'name': "POS Price Restriction 2",
    'version': '1.0',
    'depends': ['point_of_sale', 'product', 'base'],
    'author': 'Your Name',
    'category': 'Point of Sale',
    'description': """
        Restrict open price in POS based on product's min and max price.
    """,
    'data': [
        # 'views/product_template_views.xml',
    ],
    # 'assets': {
    #     'point_of_sale.assets': [
    #         # "custom_button/static/src.,
    #         # "",
    #     ],
    #     'web.assets_qweb': [
    #         '/price_restricted_2/static/src/xml/popups.xml',
    #     ],
    # },
    'installable': True,
    'application': False,
}
