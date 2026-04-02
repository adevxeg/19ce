import json
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_warehouse_id(self):
        if self.env.company.allow_sales_brand_entry and self.env.company.sales_brand_warehouse_restrict:
            self.warehouse_id = False
        else:
            super()._default_warehouse_id()

    @api.onchange('partner_id')
    def _onchange_partner_reset_warehouse(self):
        if self.env.company.allow_sales_brand_entry and self.env.company.sales_brand_warehouse_restrict:
            if self.warehouse_id not in self.partner_id.partner_warehouse_ids.mapped('warehouse_id'):
                self.warehouse_id = False

    @api.onchange('warehouse_id')
    def _onchange_warehouse_id(self):
        if self.env.company.allow_sales_brand_entry and self.env.company.sales_brand_warehouse_restrict:
            return
        else:
            super()._onchange_warehouse_id()

    @api.depends('create_uid', 'company_id', 'partner_id')
    def _compute_warehouse_id_domain(self):
        if self.env.company.allow_sales_brand_entry and self.env.company.sales_brand_warehouse_restrict:
            for rec in self:
                rec.warehouse_id_domain = [('id', 'in', rec.partner_id.partner_warehouse_ids.warehouse_id.ids)]
        else:
            super()._compute_warehouse_id_domain()
