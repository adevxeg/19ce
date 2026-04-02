from odoo.exceptions import UserError
from odoo import api, fields, models, _

class AccountPayment(models.Model):
    _inherit = "account.payment"

    bank_reference = fields.Char(string="Bank Reference", copy=False)
    cheque_reference = fields.Char(string="Cheque Reference",copy=False)
    effective_date = fields.Date(string='Effective Date', help='Effective date of PDC', copy=False)

    def print_checks(self):
        """ Check that the recordset is valid, set the payments state to
        sent and call print_checks() """
        # Since this method can be called via a client_action_multi, we
        # need to make sure the received records are what we expect
        payment_ids = self.filtered(
            lambda r: r.payment_method_id.code in ['check_printing', 'pdc'] and r.state != 'reconciled')
        if len(payment_ids) == 0:
            raise UserError(_(
                "Payments to print as a checks must have 'Check' "
                "or 'PDC' selected as payment method and "
                "not have already been reconciled"))
        if any(payment.journal_id != payment_ids[0].journal_id for payment in payment_ids):
            raise UserError(_(
                "In order to print multiple checks at once, they "
                "must belong to the same bank journal."))
        if not payment_ids[0].journal_id.check_manual_sequencing:
            # The wizard asks for the number printed on the first
            # pre-printed check so payments are attributed the
            # number of the check they'll be printed on.
            last_printed_check = payment_ids.search([
                ('journal_id', '=', payment_ids[0].journal_id.id),
                ('check_number', '!=', "0")], order="check_number desc", limit=1)
            next_check_number = last_printed_check and int(last_printed_check.check_number) + 1 or 1
            return {
                'name': _('Print Pre-numbered Checks'),
                'type': 'ir.actions.act_window',
                'res_model': 'print.prenumbered.checks',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'payment_ids': self.ids,
                    'default_next_check_number': next_check_number,
                }
            }
        else:
            self.filtered(lambda r: r.state == 'draft').post()
            self.write({'state': 'sent'})
            return self.do_print_checks()

    def _prepare_payment_moves(self):
        """ supered function to set effective date """
        res = super(AccountPayment, self)._prepare_payment_moves()
        inbound_pdc_id = self.env.ref('account_pdc.account_payment_method_pdc_in').id
        outbound_pdc_id = self.env.ref('account_pdc.account_payment_method_pdc_out').id
        if (self.payment_method_id.id == inbound_pdc_id or
                self.payment_method_id.id == outbound_pdc_id and self.effective_date):
            res[0]['date'] = self.effective_date
            for line in res[0]['line_ids']:
                line[2]['date_maturity'] = self.effective_date
        return res
