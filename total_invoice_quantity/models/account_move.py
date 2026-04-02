from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    total_product = fields.Integer(string='Total Product:', compute='_compute_total')
    total_quantity = fields.Integer(string='Total Quantity:', compute='_compute_total')

    # =========================== Compute functions =========================== #
    def _compute_total(self):
        for rec in self:
            rec.total_product = len(set(rec.invoice_line_ids.mapped('product_id')))
            rec.total_quantity = sum(rec.invoice_line_ids.mapped('quantity'))
