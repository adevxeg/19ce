from odoo.exceptions import UserError
from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):
        for rec in self:
            if rec.sale_line_id and rec.sale_line_id.order_id.sales_type == 'credit_note':
                if not self.partner_id.property_stock_customer.id:
                    raise UserError(_("You must set a Vendor Location for this partner %s", self.partner_id.name))

                warehouse_id = rec.sale_line_id.order_id.warehouse_id
                picking_type = self.env['stock.picking.type'].search(
                    [('code', '=', 'incoming'), ('warehouse_id', '=', warehouse_id.id)])
                if not picking_type:
                    picking_type = self.env['stock.picking.type'].search(
                        [('code', '=', 'incoming'), ('warehouse_id', '=', False)])
                # Update stock moves picking type, locations
                rec.picking_type_id = picking_type[:1].id
                rec.location_id = self.partner_id.property_stock_customer.id
                rec.location_dest_id = warehouse_id.lot_stock_id.id
                rec.to_refund = True
        res = super()._get_new_picking_values()
        res['note'] = self.sale_line_id.order_id.note
        return res
