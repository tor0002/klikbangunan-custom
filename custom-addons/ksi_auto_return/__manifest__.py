# -*- coding: utf-8 -*-
{
    'name': "ksi_auto_return",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_accountant','stock'],

    # always loaded
    # remember to put 'action' always in the top, because 'action' always get called
    'data': [
        'security/ir.model.access.csv',
        # 'views/auto_return_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # Whether the module should be considered as a fully-fledged application (True) or is just a technical module (False) that provides some extra functionality to an existing application module.
    # 'application' : False,
    
    # If True, this module will automatically be installed if all of its dependencies are installed.
    # 'auto_install' : False,

    # A dictionary containing python and/or binary dependencies.
    #'external_dependencies': {
    #    'python': ['ldap'],
    #},

    # If True, this module will automatically be installed if all of its dependencies are installed.
    # 'installable' : True,
}
