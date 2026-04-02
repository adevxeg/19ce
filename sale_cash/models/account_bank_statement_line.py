from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    sale_cash_in_out_account_id = fields.Many2one(comodel_name="account.account", string="Sale Cash In/Out Account")

    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        if self.sale_cash_in_out_account_id and not counterpart_account_id:
            counterpart_account_id = self.sale_cash_in_out_account_id.id
        return super()._prepare_move_line_default_vals(counterpart_account_id)