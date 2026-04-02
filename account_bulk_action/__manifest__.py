{
    'name': 'Account Bulk Action',

    'summary': '''Bulk (cancel & set to draft) invoices, bills, and entries''',
    'description': '''Bulk (cancel & set to draft) invoices, bills, and entries''',

    "author": "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['account', 'adevx_base'],
    "data": [
        # Security
        "security/ir.model.access.csv",
        "security/security.xml",
        # Views
        "views/account_move.xml",
        # Wizards
        "wizard/account_bulk_wizard.xml"
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
