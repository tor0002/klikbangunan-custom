# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Point of Sale - Extra Access Right",
    "version": "15.0.1.0.1",
    "category": "Point Of Sale",
    "summary": "Point of Sale - Extra Access Right for certain actions",
    "author": "La Louve, GRAP, Odoo Community Association (OCA), and ported by ismata aka Reza Dwiputra muridnya Mas Taqim",
    "website": "https://github.com/OCA/pos",
    "license": "AGPL-3",
    "depends": ["point_of_sale"],
    "data": [
        "security/res_groups.xml",
        "views/templates.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
    ],
    # "qweb": [
    #     "static/src/xml/*.xml",
    # ],
    "installable": True,
    'assets': {
        'point_of_sale.assets': [
            'pos_access_right/static/src/css/pos.css',
            'pos_access_right/static/src/js/models.js',
            'pos_access_right/static/src/js/ActionpadWidget.js',
            'pos_access_right/static/src/js/NumpadWidget.js',
            'pos_access_right/static/src/js/TicketScreen.js',
        ],
        'web.assets_qweb': [
            'pos_access_right/static/src/xml/**/*',
            'pos_access_right/static/src/xml/*',
            'pos_access_right/static/src/xml/*.xml',
        ],
        
    },
}
