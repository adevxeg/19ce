from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount = fields.Float(digits=False)
    amount_discount = fields.Float(string='Amount Discount')

    @api.onchange('product_uom_qty', 'price_unit', 'discount')
    def _onchange_discount(self):
        if self.discount < 0:
            raise ValidationError(_("Invalid discount amount"))
        if not self.env.context.get('from_discount_amount'):
            self.amount_discount = self.product_uom_qty * self.price_unit * (self.discount / 100)

    @api.onchange('product_uom_qty', 'price_unit', 'amount_discount')
    def _onchange_amount_discount(self):
        if self.amount_discount < 0:
            raise ValidationError(_("Invalid discount amount"))
        self_ctx = self.with_context(from_discount_amount=True)
        total_price = self_ctx.product_uom_qty * self_ctx.price_unit
        if total_price:
            self_ctx.discount = ((total_price - (total_price - self_ctx.amount_discount)) / total_price) * 100 or 0.0

    def _get_amount_discount(self):
        if self.product_id == self.env.company.sale_discount_product_id:
            return abs(self.product_uom_qty * self.price_unit)
        return self.amount_discount

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res.update({'amount_discount': self.amount_discount})
        return res
