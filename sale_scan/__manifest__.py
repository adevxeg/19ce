{
    'name': 'Sale Scan',

    'summary': 'Barcode & Code Scanning  Sale Order',
    'description': 'Barcode & Code Scanning  Sale Order',

    'author': 'Adevx',
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['sale', 'base_scan'],
    'data': [
        # Views
        'views/sale_order.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
