{
    'name': "Total Invoice Quantity",

    'summary': """Display total number of Products and Quantity on Invoices""",
    'description': """Display total number of Products and Quantity on Invoices""",

    "author": "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['account'],
    'data': [
        # Views
        'views/account_move.xml',
        # Reports
        'report/report_invoice_document.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
