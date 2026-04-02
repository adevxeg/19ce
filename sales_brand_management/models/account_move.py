from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_sales_brand_entry = fields.Boolean(string="Is Sales Brand Entry")
    is_sales_rent_entry = fields.Boolean(string="Is Sales Rent Entry")
