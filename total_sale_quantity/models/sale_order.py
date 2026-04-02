from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_sale_product = fields.Integer(string='Total Products:', compute='_compute_totals', store=True)
    total_sale_quantity = fields.Integer(string='Total Quantities:', compute='_compute_totals', store=True)

    # =========================== Compute functions =========================== #
    @api.depends('order_line')
    def _compute_totals(self):
        for rec in self:
            rec.total_sale_product = len(set(rec.order_line.mapped('product_id')))
            rec.total_sale_quantity = sum(rec.order_line.mapped('product_uom_qty'))
