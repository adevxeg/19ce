from odoo.exceptions import UserError
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_sold = fields.Float(string='Qty Sold', compute="_compute_qty_sold", store=True)
    product_variant_domain = fields.Char(related='order_id.product_variant_domain')
    product_tmpl_domain = fields.Char(related='order_id.product_tmpl_domain')

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        if self.order_id.sales_type == 'credit_note':
            self.product_uom_qty = abs(self.product_uom_qty) * -1
        else:
            self.product_uom_qty = abs(self.product_uom_qty)

    def _check_product_validity(self):
        super()._check_product_validity()
        domain = self.order_id._calc_variant_domain()
        domain.append(("id", "=", self.product_id.id))
        product_id = self.env['product.product'].search(domain)
        if not product_id:
            raise UserError(_("Product exist in system but not in domain !!"))

    @api.depends('product_id', 'product_uom_qty', 'order_partner_id', 'order_id.sales_type', 'order_id.warehouse_id')
    def _compute_qty_sold(self):
        for rec in self:
            qty_sold = 0
            if rec.order_id.sales_type == "credit_note":
                _where = f"""
                    WHERE (so.state = 'sale')
                        AND (sol.product_id={rec.product_id.id if rec.product_id else 0})
                """
                if self.env.company.force_default_credit_note_warehouse:
                    _where += f"  AND (so.warehouse_id={rec.order_id.warehouse_id.id if rec.order_id.warehouse_id else 0})"
                if self.env.company.credit_note_by_customer:
                    _where += f" AND (sol.order_partner_id={rec.order_partner_id.id if rec.order_partner_id else 0})"
                self.env.cr.execute(f"""
                    SELECT
                        CASE WHEN so.sales_type != 'credit_note' THEN SUM(sol.qty_delivered) ELSE 0 END,
                        CASE WHEN so.sales_type = 'credit_note' THEN SUM(sol.product_uom_qty) ELSE 0 END
                    FROM sale_order_line sol
                        LEFT JOIN sale_order so ON (sol.order_id=so.id)
                    """ + _where + """
                    GROUP BY so.sales_type
                """)
                qty_sold = sum([row[0] + row[1] for row in self.env.cr.fetchall()])
            rec.qty_sold = qty_sold
