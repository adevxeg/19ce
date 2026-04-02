{
    'name': "Account Move Matrix",

    'summary': """ Add variants to your account move through Grid Entry.""",
    'description': """ Add variants to your account move through Grid Entry.""",

    "author": "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['account', 'product_domain_abstract', 'product_matrix'],
    'data': [
        # Views
        'views/account_move.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'account_move_product_matrix/static/src/js/*',
            'account_move_product_matrix/static/src/xml/*',
        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
