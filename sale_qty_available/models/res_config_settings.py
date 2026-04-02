from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_order_validate_on_hand = fields.Boolean(related="company_id.sale_order_validate_on_hand", readonly=False)

