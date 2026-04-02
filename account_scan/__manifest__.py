{
    'name': 'Account Scan',

    'summary': 'Barcode & Code Scanning In Account Move',
    'description': 'Barcode & Code Scanning In  Account Move',

    'author': 'Adevx',
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['product_domain_abstract', 'base_scan', 'account'],
    'data': [
        # Views
        'views/account_move.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
