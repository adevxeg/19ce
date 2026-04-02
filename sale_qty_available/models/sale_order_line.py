from odoo import api, fields, models
from odoo.tools.sql import column_exists, create_column


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    on_hand = fields.Float(string='On-Hand', compute="_compute_on_hand", compute_sudo=True)
    free_qty = fields.Float(string='Free to Use', compute="_compute_on_hand", compute_sudo=True)


    @api.depends('product_id', 'order_id.warehouse_id', 'state')
    def _compute_on_hand(self):
        for rec in self:
            quant_ids = self.env['stock.quant'].search(
                [('location_id', 'child_of', rec.order_id.warehouse_id.lot_stock_id.id),
                 ('product_id', '=', rec.product_id.id)])
            rec.on_hand = sum(quant_ids.mapped('quantity'))
            rec.free_qty = sum(quant_ids.mapped('available_quantity'))
