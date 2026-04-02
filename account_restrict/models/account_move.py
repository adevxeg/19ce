from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'variant.domain.abstract']

    restrict_update_line_qty = fields.Boolean(string="Restrict Update Line QTy")
    allow_cancel_entry = fields.Boolean(compute="_compute_allow_cancel_entry")
    invoice_date = fields.Date(default=fields.Date.context_today)
    partner_balance_before = fields.Float(
        string="Partner Balance Before", compute="_compute_partner_balance_before")
    partner_balance = fields.Float(
        string="Partner Balance", compute="_compute_partner_balance")

    def _calc_variant_domain_depends(self):
        res = super()._calc_variant_domain_depends()
        res.extend(['partner_id'])
        return res

    def _calc_variant_domain(self):
        res = super()._calc_variant_domain()
        if self.env.user.company_id.credit_note_by_customer and self.move_type == 'out_refund':
            if self.partner_id:
                query = f""" 
                    SELECT sol.product_id 
                    FROM sale_order_line sol 
                    WHERE (sol.state = 'sale') 
                    AND (sol.order_partner_id = {self.partner_id.id})
                """
                self.env.cr.execute(query)
                res.append(("id", "in", [row[0] for row in self.env.cr.fetchall()]))
            else:
                res.append(("id", "in", []))
        return res

    @api.depends("partner_id")
    def _compute_partner_balance_before(self):
        for rec in self:
            domain = [
                ('partner_id', '=', rec.partner_id.id),
                ('account_type', 'in', ['liability_payable', 'asset_receivable']),
                ("parent_state", '=', 'posted'), ("move_id", '<', rec.id)]
            lines = self.env['account.move.line'].sudo()._read_group(domain, ['partner_id'], ['balance:sum'])
            total_balance = 0
            for partner, balance in lines:
                if rec.partner_id == partner:
                    total_balance += balance
            rec.partner_balance_before = total_balance

    @api.depends("partner_id", "state", "amount_residual")
    def _compute_partner_balance(self):
        for rec in self:
            domain = [
                ('partner_id', '=', rec.partner_id.id),
                ('account_type', 'in', ['liability_payable', 'asset_receivable']),
                ("parent_state", '=', 'posted')]
            lines = self.env['account.move.line'].sudo()._read_group(domain, ['partner_id'], ['balance:sum'])
            total_balance = 0
            for partner, balance in lines:
                if rec.partner_id == partner:
                    total_balance += balance
            rec.partner_balance = total_balance

    @api.depends('move_type')
    def _compute_allow_cancel_entry(self):
        for rec in self:
            if rec.move_type == "out_invoice" and not self.env.user.has_group('account_restrict.group_cancel_entry'):
                rec.allow_cancel_entry = False
            else:
                rec.allow_cancel_entry = True

    @api.depends('move_type', 'origin_payment_id', 'statement_line_id')
    def _compute_journal_id(self):
        super()._compute_journal_id()
        for rec in self:
            if rec.origin_payment_id or self.env.context.get('is_payment'):
                rec.journal_id = False

    def _post(self, soft=True):
        for move in self:
            if self.env.user.company_id.restrict_journal_negative_balance and move.journal_id.type in ['cash', 'bank']:
                # Compute journal running balance
                domain = [
                    ('journal_id', '=', move.journal_id.id), ('parent_state', '=', 'posted'),
                    ('account_id', '=', move.journal_id.default_account_id.id)
                ]
                totals = self.env['account.move.line'].sudo()._read_group(domain, [], ['balance:sum'])
                balance = totals[0][0]
                # Add current move lines effect
                balance += sum(move.line_ids.filtered(
                    lambda l: l.account_id == move.journal_id.default_account_id).mapped('balance'))
                if balance < 0:
                    raise ValidationError(_(
                        "You cannot post this entry because the journal '%s' "
                        "would go into negative balance."
                    ) % move.journal_id.display_name)
            if self.env.user.company_id.allow_credit_note_validate_sold_qty and move.move_type == 'out_refund':
                product_names = move.invoice_line_ids.filtered(
                    lambda x: x.sold_qty and x.quantity > x.sold_qty and x.product_id.is_storable
                ).mapped('product_id.name')
                if product_names:
                    raise ValidationError(
                        _('Quantity must be less than or equal sold qty in these lines %s') % product_names)
        return super(AccountMove, self)._post(soft)
