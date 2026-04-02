{
    'name': 'Import Sale Line',

    'summary': 'Import Sale Line',
    'description': 'Import Sale Line',

    'author': 'Adevx',
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['sale'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Wizards
        'wizard/import_sale_line.xml',
        # Views
        'views/sale_order.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
