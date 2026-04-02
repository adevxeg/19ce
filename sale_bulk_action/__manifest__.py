{
    'name': 'Sale Bulk Action',

    'summary': '''Bulk (cancel & set to draft) sale orders''',
    'description': '''Bulk (cancel & set to draft) sale orders''',

    "author": "Adevx",
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['sale_stock', 'stock_bulk_action', 'adevx_base'],
    "data": [
        # Security
        "security/ir.model.access.csv",
        "security/security.xml",
        # Views
        "views/sale_order.xml",
        # Wizards
        "wizard/sale_bulk_wizard.xml"
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
