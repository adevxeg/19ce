from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount = fields.Float(digits=False)
    amount_discount = fields.Float(string='Amount Discount')

    @api.onchange('quantity', 'price_unit', 'discount')
    def _onchange_discount(self):
        if self.discount < 0:
            raise ValidationError(_("Invalid discount amount"))
        if not self.env.context.get('from_discount_amount'):
            self.amount_discount = self.quantity * self.price_unit * (self.discount / 100)

    @api.onchange('quantity', 'price_unit', 'amount_discount')
    def _onchange_amount_discount(self):
        if self.amount_discount < 0:
            raise ValidationError(_("Invalid discount amount"))
        self_ctx = self.with_context(from_discount_amount=True)
        total_price = self_ctx.quantity * self_ctx.price_unit
        if total_price:
            self_ctx.discount = ((total_price - (total_price - self_ctx.amount_discount)) / total_price) * 100 or 0.0

    def _get_amount_discount(self):
        if self.product_id == self.env.company.account_discount_product_id:
            return abs(self.quantity * self.price_unit)
        return self.amount_discount