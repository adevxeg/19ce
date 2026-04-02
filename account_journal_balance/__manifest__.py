{
    'name': 'Account Journal Balance',

    'summary': """Account Journal Balance Calculation""",
    'description': """Account Journal Balance Calculation""",

    'author': "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['account', 'adevx_base'],
    'data': [
        # Views
        'views/res_config_settings.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
