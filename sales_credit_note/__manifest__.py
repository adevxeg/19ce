{
    'name': "Sales Credit Note",

    'summary': """Sales Credit Note""",
    'description': """Sales Credit Note""",

    'author': "Adevx",
    'category': 'Adevx/sales',
    "license": "OPL-1",
    'website': "https://adevx.com",

    'depends': ['adevx_base', 'product_domain_abstract', 'sales_auto_confirm'],
    'data': [
        # Data
        'data/ir_sequence.xml',
        # Views
        'views/sale_order.xml',
        'views/res_config_settings.xml',
        'views/res_users.xml',
        # Reports
        'report/sale_report_templates.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
