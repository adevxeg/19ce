from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_variant_domain = fields.Char(related='move_id.product_variant_domain')

    def action_register_payment(self):
        res = super().action_register_payment()
        res['context']['default_season_id'] = self.move_id.season_id.id
        return res
