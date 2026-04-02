from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_variant_domain = fields.Char(related='move_id.product_variant_domain')
    sold_qty = fields.Float(
        string='Sold Qty', compute="_compute_sold_qty",
        help="calc line sold qty using customer, customer picking, customer refund on the same location")

    @api.depends('product_id', 'quantity', 'partner_id')
    def _compute_sold_qty(self):
        for rec in self:
            sold = refund = 0
            if rec.move_id.move_type == 'out_refund' and rec.product_id and rec.partner_id:
                sold_lines = self.env['stock.move.line'].search(
                    [('picking_partner_id', '=', rec.partner_id.id), ('product_id', '=', rec.product_id.id),
                     ('state', '=', 'done'), ('picking_type_id.code', '=', 'outgoing')])
                sold = sum(sold_lines.mapped('quantity'))
                refund_lines = self.env['stock.move.line'].search(
                    [('picking_partner_id', '=', rec.partner_id.id), ('product_id', '=', rec.product_id.id),
                     ('state', '=', 'done'), ('picking_type_id.code', '=', 'incoming')])
                refund = sum(refund_lines.mapped('quantity'))
            rec.sold_qty = sold - refund
