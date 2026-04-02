from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    journal_dashboard_balance = fields.Selection(
        related="company_id.journal_dashboard_balance", readonly=False, required=True)
