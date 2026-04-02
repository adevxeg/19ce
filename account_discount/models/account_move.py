from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    account_discount_type = fields.Selection(selection=[
        ('standard', 'Standard Discount'), ('adevx', 'Adevx Discount')
    ], string="Account Discount Type", compute="_compute_account_discount_type")
    total_discount = fields.Monetary(string='Total Discount', compute='_compute_total_discount', store=True)

    def _compute_account_discount_type(self):
        for rec in self:
            rec.account_discount_type = self.env.company.account_discount_type

    @api.depends(
        'invoice_line_ids', 'invoice_line_ids.amount_discount',
        'invoice_line_ids.quantity', 'invoice_line_ids.price_unit')
    def _compute_total_discount(self):
        for rec in self:
            rec.total_discount = sum([line._get_amount_discount() for line in rec.invoice_line_ids])

    def _get_lang(self):
        self.ensure_one()
        if self.partner_id.lang and not self.partner_id.is_public:
            return self.partner_id.lang
        return self.env.lang

    @api.readonly
    def action_open_discount_wizard(self):
        self.ensure_one()
        return {
            'name': _("Discount"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.discount',
            'view_mode': 'form',
            'target': 'new',
        }