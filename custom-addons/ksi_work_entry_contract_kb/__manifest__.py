# -*- coding: utf-8 -*-
{
    'name': "ksi_work_entry_contract_kb",

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
    'depends': ['base','hr_work_entry_contract','ent_hr_employee_shift'],

    # always loaded
    # remember to put 'action' always in the top, because 'action' always get called
    'data': [
        'security/ir.model.access.csv',
        'views/hr_work_entry_type_views.xml',
        'views/hr_work_entry_views.xml',
        'views/hr_leave_views.xml',
        'data/ir_cron_data.xml',
        'views/menu_items_views.xml',


        # 'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ksi_work_entry_contract_kb/static/src/**/*',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # Whether the module should be considered as a fully-fledged application (True) or is just a technical module (False) that provides some extra functionality to an existing application module.
    # 'application' : False,
    
    # If True, this module will automatically be installed if all of its dependencies are installed.
    'auto_install' : True

    # A dictionary containing python and/or binary dependencies.
    #'external_dependencies': {
    #    'python': ['ldap'],
    #},

    # If True, this module will automatically be installed if all of its dependencies are installed.
    # 'installable' : True,
}
