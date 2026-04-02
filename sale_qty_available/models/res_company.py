from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_order_validate_on_hand = fields.Boolean(string="Sale Order Validate On-Hand", tracking=True)
