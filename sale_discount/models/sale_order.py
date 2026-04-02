from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_discount_type = fields.Selection(selection=[
        ('standard', 'Standard Discount'), ('adevx', 'Adevx Discount')
    ], string="Sale Discount Type", compute="_compute_sale_discount_type")
    total_discount = fields.Monetary(string='Total Discount', compute='_compute_total_discount', store=True)

    def _compute_sale_discount_type(self):
        for rec in self:
            rec.sale_discount_type = self.env.company.sale_discount_type

    @api.depends('order_line', 'order_line.amount_discount', 'order_line.product_uom_qty', 'order_line.price_unit')
    def _compute_total_discount(self):
        for rec in self:
            rec.total_discount = sum([line._get_amount_discount() for line in rec.order_line])
