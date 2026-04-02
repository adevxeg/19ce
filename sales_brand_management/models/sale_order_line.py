from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _calc_variant_domain(self):
        res = super()._calc_variant_domain()
        if self.env.company.allow_sales_brand_entry and self.env.company.sales_warehouse_categ_restrict:
            res.append(("categ_id", "child_of", self.order_id.warehouse_id.categ_ids.ids))
        return res