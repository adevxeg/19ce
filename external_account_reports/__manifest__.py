{
    'name': "External Account Reports",

    'summary': """External Account Reports""",
    'description': """ External Account Reports""",

    'author': "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': "https://adevx.com",

    'depends': ['account_reports'],
    'data': [
        # Views
        'views/profit_and_loss.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'external_account_reports/static/src/xml/report_filters.xml',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False
}
