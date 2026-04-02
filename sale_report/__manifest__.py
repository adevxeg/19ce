{
    'name': "Sales Report",

    'summary': """Sales Report""",
    'description': """ Sales Report""",

    'author': "Adevx",
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': "https://adevx.com",

    'depends': [
        'base_report', 'sale_stock'
    ],
    'data': [
        # Views
        'views/sale_order.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
