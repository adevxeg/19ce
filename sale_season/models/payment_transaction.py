from odoo import api, fields, models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _create_payment(self, **extra_create_values):
        payment = super()._create_payment(**extra_create_values)
        # Website Sale Payment Transaction
        if 'sale_order_ids' in self._fields:
            if self.sale_order_ids:
                payment.sudo().write({
                    'season_id': self.sale_order_ids[-1].season_id.id
                })
        return payment
