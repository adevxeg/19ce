from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _name = 'account.bank.statement.line'
    _inherit = ['account.bank.statement.line', 'season.abstract']

    @api.model_create_multi
    def create(self, vals_list):
        # Create account bank statement lines
        records = super().create(vals_list)
        for rec in records:
            # Update account bank statement line [account move] season_id
            if rec.move_id and rec.move_id.season_id != rec.season_id:
                rec.move_id.sudo().write({
                    'season_id': rec.season_id.id
                })
        return records
