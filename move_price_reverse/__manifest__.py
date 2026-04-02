{
    'name': "Move Price Reverse",

    'summary': """Account Move Line Price Reverse""",
    'description': """Account Move Line Price Reverse""",

    'author': "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['account', 'adevx_base'],
    'data': [
        # Views
        'views/res_config_settings.xml',
        'views/account_move.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
