from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    credit_note_by_customer = fields.Boolean(string="Credit Note By Customer", default=True, tracking=True)
    credit_note_validate_qty_sold = fields.Boolean(string="Credit Note Validate Qty Sold", default=True, tracking=True)
    sale_warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse", string="Default Sales Warehouse", tracking=True)
    force_default_sale_warehouse = fields.Boolean(string="Force Sales Warehouse", tracking=True)
    credit_note_warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse", string="Default Credit Note Warehouse", tracking=True)
    force_default_credit_note_warehouse = fields.Boolean(string="Force Default Credit Note Warehouse", tracking=True)



