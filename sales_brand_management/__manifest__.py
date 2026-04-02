{
    'name': "Sales Brand Management",

    'summary': """Sales Brand Management""",
    'description': """Sales Brand Management""",

    'author': "Adevx",
    'category': 'Adevx/sales',
    'license': "OPL-1",
    'website': "https://adevx.com",

    'depends': ['adevx_base', 'sales_credit_note'],
    'data': [
        # Data
        'data/sales_brand_entry_cron.xml',
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/res_partner.xml',
        'views/res_partner_category.xml',
        'views/res_config_settings.xml',
        'views/stock_warehouse.xml',
        # Reports
        'report/sales_brand_report.xml',
        # Wizards
        'wizard/sales_brand_report_wizard.xml'

    ],
    "assets": {
        'web.report_assets_common': [
            "sales_brand_management/static/src/scss/sales_brand_report.scss",
        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
