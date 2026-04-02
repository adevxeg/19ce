from odoo import api, fields, models, tools


class SalesBrandReport(models.Model):
    _name = "sales.brand.report"
    _description = "Sales Brand Report"
    _auto = False

    date = fields.Datetime(string="Date", readonly=True)
    partner_id = fields.Many2one(string="Partner", comodel_name="res.partner", readonly=True)
    commission_amount = fields.Float(string="Commission Amount", readonly=True)
    tax_amount = fields.Float(string="Tax Amount", readonly=True)

    def init_results(self, filters):
        brand_tax_amount = 0
        brand_tax_lines = self.env.company.sales_brand_ids.filtered(lambda b: b.type == "tax")
        if brand_tax_lines:
            brand_tax_amount = brand_tax_lines[0].tax_id.amount
        query_ = """
            SELECT 
                row_number() OVER () AS id,
                * 
            FROM(
                SELECT 
                    rp.id AS partner_id,
                    DATE(so.date_order) AS date,
                    COALESCE(SUM((sol.price_subtotal / NULLIF(sol.product_uom_qty, 0)) * sol.qty_delivered * rp.sales_perc / 100), 0) AS commission_amount,
                    (CASE WHEN NOT rp.skip_tax AND %s > 0
                      THEN COALESCE(SUM((sol.price_subtotal / NULLIF(sol.product_uom_qty, 0)) * sol.qty_delivered * %s / 100), 0)
                      ELSE 0
                      END) AS tax_amount
                FROM sale_order_line sol
                    LEFT JOIN stock_move st on (sol.id=st.sale_line_id)
                    LEFT JOIN sale_order so ON (sol.order_id=so.id)
                    LEFT JOIN res_partner rp ON (so.partner_id=rp.id)
                WHERE st.state = 'done'
                    AND rp.id  in %s
                    AND so.date_order >= %s 
                    AND so.date_order <= %s
                GROUP BY rp.id, DATE(so.date_order)
            ) AS a
            ORDER BY a.partner_id, a.date
        """
        params = (
            brand_tax_amount,
            brand_tax_amount,
            tuple(filters.get("partner_ids")),
            filters.get("start_date"),
            filters.get("end_date")
        )
        tools.drop_view_if_exists(self.env.cr, self._table)
        res = self.env.cr.execute("""CREATE VIEW {} AS ({})""".format(self._table, query_), params)
        return res

    def view_report_details(self, filters):
        self.init_results(filters)
        details = self.search([])
        data = {
            'start_date': filters.get('start_date'),
            'end_date': filters.get('end_date'),
            'partner_names': filters.get('partner_names'),
            'detail_ids': details.ids
        }
        return self.env.ref('sales_brand_management.action_sales_brand_report_html').with_context(
            active_model="sales.brand.report").report_action(details.ids, data=data)