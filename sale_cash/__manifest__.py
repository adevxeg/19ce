{
    'name': "Sale Cash",

    'summary': """Sale Cash In/Out""",
    'description': """Sale Cash In/Out""",

    'author': "Adevx",
    'category': "Adevx/sales",
    "license": "OPL-1",
    'website': "https://adevx.com",

    'depends': ['sale'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/account_account.xml',
        # Wizards
        'wizard/cash_in_out.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
