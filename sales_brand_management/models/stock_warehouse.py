from odoo import fields, models, api


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    categ_ids = fields.Many2many(comodel_name='product.category', string='Product Categories')
