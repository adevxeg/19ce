from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):
    _name = 'account.payment.register'
    _inherit = ['account.payment.register', 'season.abstract']

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super()._create_payment_vals_from_wizard(batch_result)
        res['season_id'] = self.season_id.id
        return res

    def _create_payment_vals_from_batch(self, batch_result):
        res = super()._create_payment_vals_from_batch(batch_result)
        res['season_id'] = self.season_id.id
        return res
