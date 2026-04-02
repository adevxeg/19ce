{
    'name': 'Account PDC',

    'summary': """ Extension on Cheques to handle Post Dated Cheques """,
    'description': """ Extension on Cheques to handle Post Dated Cheques """,

    'author': "Adevx",
    'category': 'Adevx/accounting',
    "license": "OPL-1",
    'website': 'https://adevx.com',

    'depends': ['account_check_printing', 'sale'],
    'data': [
        # Data
        'data/account_payment_method.xml',
        # Views
        'views/account_payment.xml',
        'views/account_payment_register.xml',
        'views/sale_order.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
