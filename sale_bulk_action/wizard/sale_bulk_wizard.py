from odoo.exceptions import UserError
from odoo import api, fields, models, _


class SaleBulkWizard(models.TransientModel):
    _name = "sale.bulk.wizard"
    _description = 'Bulk Action Wizard for Sale Orders'

    order_ids = fields.Many2many('sale.order', string="Selected Orders")
    action_type = fields.Selection(
        selection=[('draft', 'Set to Draft'), ('cancel', 'Cancel')], string="Action", required=True)

    def action_confirm(self):
        self.ensure_one()
        if not self.order_ids:
            raise UserError(_("No records selected."))
        to_unlock = self.order_ids.filtered(lambda o: o.locked)
        to_unlock.action_unlock()
        if self.action_type == 'draft':
            self.order_ids.action_draft()
        elif self.action_type == 'cancel':
            self.order_ids.action_cancel()