from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    price_margin = fields.Float(groups="account_margin.group_account_margin")
    inventory_value = fields.Float(groups="product_base.group_product_cost")
