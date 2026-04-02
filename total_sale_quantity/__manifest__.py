{
    'name': "Total Sale Quantity",

    'summary': """Display Total Number Of Products And Quantity On RFQ / Sale Order""",
    'description': """Display Total Number Of Products And Quantity On RFQ / Sale Order""",

    "author": "Adevx",
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['sale'],
    'data': [
        # Views
        'views/sale_order.xml',
        # Reports
        'report/sale_report_templates.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
