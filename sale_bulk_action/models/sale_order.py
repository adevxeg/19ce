from odoo import api, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_payment_ids(self, invoice):
        payment = invoice.invoice_payments_widget
        payment_ids = []
        if payment:
            for pay in payment.get('content'):
                if pay.get('account_payment_id'):
                    payment_ids.append(pay.get('account_payment_id'))
            if payment_ids:
                payment_ids = self.env['account.payment'].browse(payment_ids)
                return payment_ids
        return payment_ids

    def unlink(self):
        for sale in self:
            if sale.picking_ids or sale.invoice_ids:
                raise ValidationError(_('Please unlink all pickings and invoices for this order first !'))
        return super(SaleOrder, self).unlink()

    def action_cancel(self):
        if self.picking_ids:
            for picking in self.picking_ids:
                if picking.state != 'cancel':
                    picking.action_cancel()
        if self.invoice_ids:
            for invoice in self.invoice_ids:
                if invoice.state != 'cancel':
                    payment_ids = self.get_payment_ids(invoice)
                    if payment_ids:
                        for payment in payment_ids:
                            payment.action_cancel()
                    invoice.button_cancel()
        return super(SaleOrder, self).action_cancel()



