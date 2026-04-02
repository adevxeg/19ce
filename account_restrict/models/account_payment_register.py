from odoo import api, fields, models, _


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.depends('available_journal_ids')
    def _compute_journal_id(self):
        super()._compute_journal_id()
        for rec in self:
            rec.journal_id = False
