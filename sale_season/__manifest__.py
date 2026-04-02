{
    'name': "Sale Season",

    'summary': """Sale Season""",
    'description': """Sale Season""",

    'author': "Adevx",
    'category': 'Adevx/sales',
    'license': "OPL-1",
    'website': "https://adevx.com",

    'depends': ['sale_stock', 'account_season', 'stock_season', 'sale_report'],
    'data': [
        # Views
        'views/sale_order.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
