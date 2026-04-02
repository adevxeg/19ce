from odoo.exceptions import UserError
from odoo import api, models, fields, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    margin = fields.Monetary(groups="so_margin.group_sale_margin")
    margin_percent = fields.Float(groups="so_margin.group_sale_margin")
