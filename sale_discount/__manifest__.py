{
    'name': "Sale Discount",

    'summary': """Sale Order Discount""",
    'description': """Sale Order Discount""",

    'author': "Adevx",
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': "https://adevx.com",

    'depends': ['sale', 'adevx_base', 'account_discount'],
    'data': [
        # Views
        'views/sale_order.xml',
        'views/res_config_settings.xml',
        # Wizards
        'wizard/sale_order_discount.xml',
        # Reports
        'report/report_saleorder_document.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
