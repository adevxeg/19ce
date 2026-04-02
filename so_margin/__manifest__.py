{
    'name': 'Sale Margin',

    'summary': 'Sale Order Margin Control',
    'description': 'Sale Order Margin Control',

    'author': 'Adevx',
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['sale_margin', 'product_base'],
    'data': [
        # Security
        'security/security.xml',
        # Views
        'views/sale_order.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
