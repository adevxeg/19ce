from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _auto_confirm_picking(self):
        # Validate Picking_ids
        for picking in self.picking_ids:
            picking.action_assign()
            picking.button_validate()

    def _auto_confirm_invoice(self, final=False):
        # Create And Validate Invoice
        self._create_invoices(final=final)
        for invoice in self.invoice_ids:
            if not invoice.invoice_date:
                invoice.invoice_date = fields.Date.context_today(self)
            invoice.action_post()

    def _auto_confirm_one_step(self):
        if self.env.company.one_step_sale:
            self._auto_confirm_picking()
            self._auto_confirm_invoice()

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self._auto_confirm_one_step()
        return res
