from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    margin = fields.Float(groups="so_margin.group_sale_margin")
