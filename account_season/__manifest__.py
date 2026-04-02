{
    'name': "Account Season",

    'summary': """Account Season""",
    'description': """Account Season""",

    'author': "Adevx",
    'category': 'Adevx/accounting',
    'license': "OPL-1",
    'website': "https://adevx.com",

    'depends': ['account', 'base_season', 'product_domain_abstract', 'adevx_base'],
    'data': [
        # Views
        'views/account_move.xml',
        'views/account_payment_register.xml',
        'views/account_payment.xml',
        'views/res_config_settings.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
