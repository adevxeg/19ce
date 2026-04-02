from odoo import api, models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        if self.env.company.sale_order_validate_on_hand:
            if self and not self.order_line:
                raise UserError("Please add lines first !!")
            if any(l.product_uom_qty > l.free_qty and l.product_id.is_storable for l in self.order_line):
                raise UserError('Please check Free to Use quantity to Complete Order!!')
        return super(SaleOrder, self).action_confirm()
