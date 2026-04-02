{
    'name': 'Sale Order Catalog',

    'summary': 'Sale Order Catalog',
    'description': 'Sale Order Catalog',

    'author': "Adevx",
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': "https://adevx.com",

    'depends': ['sale_stock'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Wizards
        'wizard/catalog_order_wizard.xml',
        # Views
        'views/product_product.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sale_order_catalog/static/src/**/*'
        ]
    },

    'installable': True,
    'application': False,
    'auto_install': False,
}
