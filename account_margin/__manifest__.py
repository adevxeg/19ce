{
    'name': "Account Margin",

    'summary': """Account Margin""",
    'description': """Account Margin""",

    'author': "Adevx",
    'category': 'Adevx/accounting',
    'license': "OPL-1",
    'website': "https://adevx.com",

    'depends': ['stock_account', 'product_base'],
    'data': [
        # Security
        'security/security.xml',
        # Views
        'views/product_product.xml',
        'views/stock_quant.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
