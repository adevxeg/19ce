from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    credit_note_by_customer = fields.Boolean(
        related="company_id.credit_note_by_customer", readonly=False)
    allow_credit_note_validate_sold_qty = fields.Boolean(
        related="company_id.allow_credit_note_validate_sold_qty", readonly=False)
    restrict_journal_negative_balance = fields.Boolean(
        related="company_id.restrict_journal_negative_balance", readonly=False)
