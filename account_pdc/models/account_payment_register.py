from odoo import api, fields, models, _


class AccountRegisterPayments(models.TransientModel):
    _inherit = "account.payment.register"

    bank_reference = fields.Char(string="Bank Reference", copy=False)
    cheque_reference = fields.Char(string="Cheque Reference", copy=False)
    effective_date = fields.Date(string='Effective Date', help='Effective date of PDC', copy=False)

    def _prepare_payment_vals(self, invoices):
        """Its prepare the payment values for the invoice and update the MultiPayment"""
        res = super(AccountRegisterPayments, self)._prepare_payment_vals(invoices)
        # Check payment method is Check or PDC
        check_pdc_ids = self.env['account.payment.method'].search([('code', 'in', ['pdc', 'check_printing'])])
        if self.payment_method_id.id in check_pdc_ids.ids:
            currency_id = self.env['res.currency'].browse(res['currency_id'])
            journal_id = self.env['account.journal'].browse(res['journal_id'])
            # Updating values in case of Multi payments
            res.update({
                'bank_reference': self.bank_reference,
                'cheque_reference': self.cheque_reference,
                'check_manual_sequencing': journal_id.check_manual_sequencing,
                'effective_date': self.effective_date,
                'check_amount_in_words': currency_id.amount_to_text(res['amount']),
            })
        return res

    def _create_payment_vals_from_wizard(self, batch_result):
        """It super the wizard action of the creation payment values and update the bank and check values"""
        res = super(AccountRegisterPayments, self)._create_payment_vals_from_wizard(batch_result)
        if self.effective_date:
            res.update({
                'bank_reference': self.bank_reference,
                'cheque_reference': self.cheque_reference,
                'effective_date': self.effective_date,
            })
        return res

    def _create_payment_vals_from_batch(self, batch_result):
        """It super the batch action of the creation payment values and update  the bank and check values"""
        res = super(AccountRegisterPayments, self)._create_payment_vals_from_batch(batch_result)
        if self.effective_date:
            res.update({
                'bank_reference': self.bank_reference,
                'cheque_reference': self.cheque_reference,
                'effective_date': self.effective_date,
            })
        return res

    def _create_payments(self):
        """USed to create a list of payments and update the bank and check reference"""
        payments = super(AccountRegisterPayments, self)._create_payments()
        for payment in payments:
            payment.write({
                'bank_reference': self.bank_reference,
                'cheque_reference': self.cheque_reference
            })
        return payments

