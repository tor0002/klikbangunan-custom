{
    'name': "Dynamic Approval Purchase Order",

    'summary': """
        Created for company with dynamic approval on Purchase Order.""",

    'description': """
        This module can setting approval for Purchase Order depending by Range of maximum order.
    """,

    'author': "PT. ISMATA NUSANTARA ABADI",
    'website': "http://www.ismata.co.id",

    'category': 'Purchases',
    'license': 'OPL-1',
    'version': '1.0',
    'price': '23.50',
    'currency': 'USD',
    'support': 'admin@ismata.co.id',
    'images': ['static/description/companies.png'],
    'depends': ['base', 'purchase'],

    'data': [
        'security/ir.model.access.csv',
        'views/company.xml',
        'views/purchase.xml',
        'wizard/wizard.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}
