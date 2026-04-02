{
    'name': "Account Discount",

    'summary': """Account Move Discount""",
    'description': """Account Move Discount""",

    'author': "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': "https://adevx.com",

    'depends': ['account', 'adevx_base'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/account_move.xml',
        'views/res_config_settings.xml',
        # Wizards
        'wizard/account_move_discount.xml',
        # Reports
        'report/report_invoice_document.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
