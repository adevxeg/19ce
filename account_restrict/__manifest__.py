{
    'name': "Account Restrict",

    'summary': """In this module Control customer invoice,vendor bill, open partner refund""",
    'description': """In this module Control customer invoice,vendor bill, open partner refund""",

    'author': "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['sale_stock', 'purchase', 'adevx_base', 'product_domain_abstract'],
    'data': [
        # Security
        'security/security.xml',
        # Views
        'views/res_config_settings.xml',
        'views/stock_picking.xml',
        'views/account_move.xml',
        'views/res_partner.xml',
        'views/menus.xml',
        # Reports
        'report/report_invoice_document.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
