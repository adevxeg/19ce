from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bill_refund_by_season = fields.Boolean(related="company_id.bill_refund_by_season", readonly=False)
