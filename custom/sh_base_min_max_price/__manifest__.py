# __manifest__.py
{
    'name': 'Base Min Max Price',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Base module to handle min max pricing logic',
    'description': 'This module provides base functionalities for handling minimum and maximum pricing for products.',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'depends': ['base', 'product'],
    'data': [
        'views/product_min_max_views.xml',],
    'installable': True,
    'application': False,
}
