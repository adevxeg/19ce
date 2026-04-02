{
    'name': 'Sale Qty Available',

    'summary': 'Qty Available In Sale Order',
    'description': 'Qty Available In Sale Order',

    'author': 'Adevx',
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['sale_stock'],
    'data': [
        # Views
        'views/sale_order.xml',
        'views/res_config_settings.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
