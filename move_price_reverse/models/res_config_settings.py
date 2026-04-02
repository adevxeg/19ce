from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_reverse_calc = fields.Boolean(related="company_id.invoice_reverse_calc", readonly=False)
