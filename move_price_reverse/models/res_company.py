from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_reverse_calc = fields.Boolean(string="Invoice Reverse Calculation")
