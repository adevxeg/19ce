from odoo import api, fields, models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'season.abstract']

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res['season_id'] = self.season_id.id
        return res

    def _get_action_view_picking(self, pickings):
        res = super()._get_action_view_picking(pickings)
        res['context']['default_season_id'] = self.season_id.id
        return res
