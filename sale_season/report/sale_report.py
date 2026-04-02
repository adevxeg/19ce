from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    season_id = fields.Many2one(comodel_name="season.season", string="Season", readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['season_id'] = "s.season_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,s.season_id"""
        return res
