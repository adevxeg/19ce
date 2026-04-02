from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_discount_product_id = fields.Many2one(related='company_id.account_discount_product_id', readonly=False)
    account_discount_type = fields.Selection(related="company_id.account_discount_type", readonly=False)