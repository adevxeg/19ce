from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    total_sale_quantity = fields.Integer(string='Total Quantities')

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['total_sale_quantity'] = "s.total_sale_quantity"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,s.total_sale_quantity"""
        return res
