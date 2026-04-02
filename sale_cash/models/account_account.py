from odoo import api, fields, models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    sale_is_cash_in_out = fields.Boolean(string="Sale Is Cash In/Out")

