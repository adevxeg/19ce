from odoo import api, fields, models


class AccountPayment(models.Model):
    _name = 'account.payment'
    _inherit = ['account.payment', 'season.abstract']

    @api.model_create_multi
    def create(self, vals_list):
        # Create account payment
        records = super().create(vals_list)
        for rec in records:
            # Update account payment [account move] season_id
            if rec.move_id and rec.move_id.season_id != rec.season_id:
                rec.move_id.sudo().write({
                    'season_id': rec.season_id.id
                })
        return records
