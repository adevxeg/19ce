from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.constrains('total_discount')
    def _validate_sale_discount(self):
        for rec in self:
            sale_orders = rec.invoice_line_ids.sale_line_ids.order_id
            if sale_orders:
                if rec.total_discount != sum(order.total_discount for order in sale_orders):
                    raise ValidationError(_(
                        "You can not change discount on invoice lines that are created from sale order."))
