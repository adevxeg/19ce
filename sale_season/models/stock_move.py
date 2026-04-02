from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):
        res = super()._get_new_picking_values()
        if self.mapped('sale_line_id') and self.mapped('sale_line_id.order_id'):
            res['season_id'] = self.mapped('sale_line_id.order_id.season_id').id
        return res
