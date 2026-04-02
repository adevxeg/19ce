{
    'name': "Account Partner Reports",

    'summary': """Add Smart Buttons in Partner for (Partner Ledger, and Journal Items).""",
    'description': """Add Smart Buttons in Partner for (Partner Ledger, and Journal Items).""",

    "author": "Adevx",
    'category': 'Adevx/accounting',
    "license": "OEEL-1",
    'website': 'https://adevx.com',

    'depends': ['account_reports'],
    'data': [
        # Views
        'views/res_partner.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
