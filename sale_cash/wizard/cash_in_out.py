from odoo.exceptions import UserError
from odoo import api, fields, models, _


class CashInOut(models.Model):
    _name = 'cash.in.out'
    _description = 'Cash In Out'

    amount = fields.Float(string="Amount")
    account_id = fields.Many2one(
        comodel_name="account.account", string="Account", required=True, domain=[("sale_is_cash_in_out", '=', True)])
    reason = fields.Text(string="Reason", required=True)
    sale_cash_in_out_journal_id = fields.Many2one(comodel_name="account.journal", string="Cash in/out Journal")

    def action_cash_in(self):
        self._try_cash_in_out("in")

    def action_cash_out(self):
        self._try_cash_in_out("out")

    def _try_cash_in_out(self, _type):
        sign = -1 if _type == 'in' else 1
        if not self.sale_cash_in_out_journal_id:
            raise UserError(_(f"There is no cash in/out journal"))
        if self.amount <= 0:
            raise UserError(_("Cash in/out amount must be greater than Zero !!"))
        self.env['account.bank.statement.line'].create({
            'journal_id': self.sale_cash_in_out_journal_id.id,
            'sale_cash_in_out_account_id': self.account_id.id,
            'amount': sign * self.amount,
            'date': fields.Date.context_today(self),
            'payment_ref': self.reason,
        })






