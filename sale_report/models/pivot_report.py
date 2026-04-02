from odoo import models, fields, api


class PivotReport(models.Model):
    _inherit = 'pivot.report'

    order_type = fields.Selection(selection_add=[('so', 'Sales Order')])
    order_state = fields.Selection(selection_add=[('sale', 'Sales Order')])

    def _select_additional_sale_fields(self):
        all_fields = self._select_base_fields()
        price_total = "CASE WHEN rc.report_prices = 'tax_excluded' THEN sol.price_subtotal ELSE sol.price_total END"
        all_fields.update({
            'date': 'so.date_order',
            'order_name': "so.name",
            'order_type': "'so'",
            'order_state': 'so.state',
            'warehouse_id': 'sw.id',
            'company_id': 'rc.id',
            'customer_id': 'so.partner_id',
            'total_discount': 'COALESCE(SUM(sol.price_unit * sol.qty_delivered * sol.discount / 100), 0)',
            'margin': 'COALESCE(SUM(sol.margin), 0)',
            'margin_perc': "COALESCE(SUM(sol.margin_percent), 0)",
            'sale_qty': "(CASE WHEN SIGN(sol.product_uom_qty) = 1 THEN COALESCE(SUM(sol.qty_delivered), 0) ELSE 0 END)",
            'sale_price_total': f"(CASE WHEN SIGN(sol.product_uom_qty) = 1 THEN COALESCE(SUM({price_total} / sol.product_uom_qty * sol.qty_delivered), 0) ELSE 0 END)",
            'sale_cost': "(CASE WHEN SIGN(sol.product_uom_qty) = 1 THEN COALESCE(SUM(sol.purchase_price * sol.qty_delivered), 0) ELSE 0 END)",
            'ret_sale_qty': "(CASE WHEN SIGN(sol.product_uom_qty) = -1 THEN COALESCE(SUM(sol.qty_delivered * -1), 0) ELSE 0 END)",
            'ret_sale_price_total': f"(CASE WHEN SIGN(sol.product_uom_qty) = -1 THEN COALESCE(SUM({price_total} / sol.product_uom_qty * sol.qty_delivered * -1), 0) ELSE 0 END)",
            'ret_sale_cost': "(CASE WHEN SIGN(sol.product_uom_qty) = -1 THEN COALESCE(SUM(sol.purchase_price * sol.qty_delivered * -1), 0) ELSE 0 END)",
            'net_sale_qty': "COALESCE(SUM(sol.qty_delivered), 0)",
            'net_sale_price_total': f"COALESCE(SUM({price_total} / sol.product_uom_qty * sol.qty_delivered), 0)",
            'net_sale_cost': "COALESCE(SUM(sol.purchase_price * sol.qty_delivered), 0)",
        })
        return all_fields

    @api.model
    def _sale_select(self):
        _select = ""
        select_additional_fields = self._select_additional_sale_fields()
        for field, value in select_additional_fields.items():
            if not _select:
                _select += f"SELECT {value} AS {field}"
            else:
                _select += f", {value} AS {field}"
        return _select

    @api.model
    def _sale_from(self):
        shared_from = self._from()
        shared_from += """
            LEFT JOIN sale_order_line sol ON pp.id = sol.product_id
            LEFT JOIN sale_order so ON sol.order_id = so.id
            LEFT JOIN res_company rc ON so.company_id = rc.id
            LEFT JOIN stock_warehouse sw ON so.warehouse_id = sw.id
        """
        return shared_from

    @api.model
    def _sale_where(self):
        return """
            WHERE pp.product_tmpl_id IS NOT NULL
                AND so.state = 'sale'
        """

    @api.model
    def _stock_where(self):
        stock_where_ = super()._stock_where()
        stock_where_ += """
            AND sp.sale_id IS NULL
        """
        return stock_where_

    @api.model
    def _sale_group_by(self):
        return """
            GROUP BY
                pp.id,
                pt.id,
                pc.id,
                sw.id,
                rc.id,
                so.id,
                so.name,
                so.state,
                so.date_order,
                sol.product_uom_qty
        """

    @property
    def _sale_query(self):
        return "%s %s %s %s" % (self._sale_select(), self._sale_from(), self._sale_where(), self._sale_group_by())

    def _union_from(self):
        union_from = super()._union_from()
        union_from += """
            UNION ALL
            %s
        """ % self._sale_query
        return union_from

