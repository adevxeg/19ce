from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_discount_product_id = fields.Many2one(
        string="Sale Discount Product", related='company_id.sale_discount_product_id', readonly=False)
    sale_discount_type = fields.Selection(related="company_id.sale_discount_type", readonly=False)
