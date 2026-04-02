from odoo import fields, models, api


class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ['stock.move', 'template.domain.abstract']

    def _calc_variant_domain(self):
        res = super()._calc_variant_domain()
        if self.env.company.allow_sales_brand_entry and self.partner_id:
            res.append(("categ_id", "child_of", self.partner_id.partner_warehouse_ids.warehouse_id.categ_ids.ids))
        return res
