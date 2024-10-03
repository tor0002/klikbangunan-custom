# Part of Softhealer Technologies.

{
    'name': 'Set Minimum and Maximum Price on POS Product | Point Of Sale Product Minimum Price | Point Of Sale Product Maximum Price',

    'author': 'Softhealer Technologies',

    "license": "OPL-1",

    'website': 'https://www.softhealer.com',

    'support': 'support@softhealer.com',

    'version': '15.0.1',

    'category': 'Point Of Sale',

    'summary': "Set Minimum Product Price Set Maximum Product Price Manage Product Pricelist Management Min Product Price Max Product Price POS Product Min Price POS Product Max Price Point Of Sale Product Min Price Point Of Sale Product Max Price Odoo",

    'description': """This module is useful to set minimum and maximum selling price for the product at the point of sale. POS user can see the minimum and maximum sale price so that will use to make clear action in sales procedure without waiting for a senior person. It generates a warning if POS users make orders with a different price than the min-max pricing.""",
    'depends': ['point_of_sale', 'sh_base_min_max_price'],
    'application': True,
    'data': ['security/pos_group.xml', ],
    'assets': {'point_of_sale.assets': ['sh_pos_min_max_price/static/src/js/pos.js', ], },
    'auto_install': False,
    'installable': True,
    "images": ["static/description/background.png", ],
    "price": 20,
    "currency": "EUR"
}
