from odoo.exceptions import UserError
from odoo import api, fields, models, _


class AccountBulkWizard(models.TransientModel):
    _name = "account.bulk.wizard"
    _description = 'Bulk Action Wizard for Invoices'

    move_ids = fields.Many2many('account.move', string="Selected Moves")
    action_type = fields.Selection(
        selection=[('draft', 'Set to Draft'), ('cancel', 'Cancel')], string="Action", required=True)

    def action_confirm(self):
        self.ensure_one()
        if not self.move_ids:
            raise UserError(_("No records selected."))
        if self.action_type == 'draft':
            to_draft = self.move_ids.filtered(lambda move: move.state in ('cancel', 'posted'))
            to_draft.button_draft()
        elif self.action_type == 'cancel':
            self.move_ids.button_cancel()