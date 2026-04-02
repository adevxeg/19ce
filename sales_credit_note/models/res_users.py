from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_sale_warehouse_by_user = fields.Boolean(string="Restrict Sale Warehouse By User")
    allowed_warehouse_ids = fields.Many2many(comodel_name="stock.warehouse", string="Allowed Warehouses")