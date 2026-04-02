from collections import defaultdict
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = "res.partner"

    skip_tax = fields.Boolean(string="Skip Brand Tax", tracking=True)
    sales_perc = fields.Float(string="Brand Sales (%)", tracking=True)
    partner_warehouse_ids = fields.One2many(
        comodel_name='partner.warehouse', inverse_name='partner_id', string='Warehouses')

    @api.onchange('sales_perc')
    def _onchange_sales_perc(self):
        if self.sales_perc and 0 > self.sales_perc > 100:
            raise ValidationError(_("Brand Sales (%) must be between 0 and 100"))

    def _get_sales_brand_entry_dates(self, days):
        now = fields.Datetime.now()
        current_day = now.day
        scheduled_days = sorted(eval(days))
        if current_day not in scheduled_days:
            return None, None
        # End date
        end_date = now
        # Start date
        current_index = scheduled_days.index(current_day)
        if current_index == 0:
            start_day = scheduled_days[-1]
            if start_day >= current_day:
                start_date = end_date - relativedelta(months=1)
                start_date = start_date.replace(day=start_day)
            else:
                start_date = end_date.replace(day=start_day)
        else:
            start_day = scheduled_days[current_index - 1]
            start_date = end_date.replace(day=start_day)

        return start_date, end_date

    def _get_sales_rent_entry_dates(self, days):
        now = fields.Datetime.now()
        current_day = now.day
        days = sorted(eval(days))
        if current_day not in days:
            return False
        return True

    def _prepare_sales_brand_entry_lines(self, start_date, end_date):
        # Query data
        query = f"""
            SELECT 
                so.partner_id AS partner_id,
                COALESCE(SUM((sol.price_subtotal / NULLIF(sol.product_uom_qty, 0)) * sol.qty_delivered), 0) AS total
            FROM sale_order_line sol
                LEFT JOIN stock_move st ON (sol.id=st.sale_line_id)
                LEFT JOIN sale_order so ON (sol.order_id=so.id)
            WHERE st.state = 'done'
                AND so.partner_id IS NOT NULL
                AND so.date_order >= '{start_date}'
                AND so.date_order <= '{end_date}'
            GROUP BY so.partner_id
        """
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()
        # Prepare brand entry lines
        labels, lines = {}, {}
        for line in self.env.company.sales_brand_ids:
            journal_id = line.journal_id.id
            for partner_id, total in result:
                partner = self.env['res.partner'].browse(partner_id)
                # Prepare debit, credit lines
                if line.type == 'commission':
                    line_value = total * partner.sales_perc / 100
                else:
                    line_value = 0
                    if not partner.skip_tax:
                        line_value = total * line.tax_id.amount / 100
                if line_value == 0:
                    continue
                detail_lines = [
                    (0, 0, {
                        'name': f"{line.name}",
                        'partner_id': partner_id,
                        'account_id': line.debit_account_id.id,
                        'debit': round(line_value, 2) if line_value > 0 else 0,
                        'credit': abs(round(line_value, 2)) if line_value < 0 else 0
                    }),
                    (0, 0, {
                        'name': f"{line.name}",
                        'partner_id': partner_id,
                        'account_id': line.credit_account_id.id,
                        'debit': abs(round(line_value, 2)) if line_value < 0 else 0,
                        'credit': round(line_value, 2) if line_value > 0 else 0
                    })
                ]
                if journal_id not in lines:
                    lines[journal_id] = detail_lines
                else:
                    lines[journal_id].extend(detail_lines)
            if lines:
                if journal_id not in labels:
                    labels[journal_id] = line.name
                else:
                    labels[journal_id] += "-" + line.name
        return labels, lines

    def _prepare_sales_rent_entry_lines(self):
        # Query data
        query = """
            SELECT 
                pw.partner_id AS partner_id,
                sw.id AS warehouse_id,
                sw.name AS warehouse_name,
                COALESCE(SUM(pw.rent_amount), 0) AS rent
            FROM partner_warehouse pw
                LEFT JOIN stock_warehouse sw ON (pw.warehouse_id=sw.id)
            WHERE pw.rent_amount > 0
            GROUP BY pw.partner_id, sw.id, sw.name
        """
        self.env.cr.execute(query)
        # Group query data per partner
        partners_grouped = defaultdict(list)
        for item in self.env.cr.dictfetchall():
            partners_grouped[item['partner_id']].append(item)
        # Prepare rent entry lines
        lines =  []
        for partner_id, partner_data in dict(partners_grouped).items():
            # Group partner data per warehouse
            warehouse_grouped = defaultdict(list)
            for item in partner_data:
                warehouse_grouped[item['warehouse_id']].append(item)
            for warehouse_id, warehouse_data in dict(warehouse_grouped).items():
                for rec in warehouse_data:
                    lines.extend([
                        (0, 0, {
                            'name': f"Rent for Warehouse: {rec['warehouse_name']}",
                            'partner_id': partner_id,
                            'account_id': self.env.company.sales_rent_debit_account_id.id,
                            'debit': round(rec['rent'], 2) if rec['rent'] > 0 else 0,
                            'credit': abs(round(rec['rent'], 2)) if rec['rent'] < 0 else 0
                        }),
                        (0, 0, {
                            'name': f"Rent for Warehouse: {rec['warehouse_name']}",
                            'partner_id': partner_id,
                            'account_id': self.env.company.sales_rent_credit_account_id.id,
                            'debit': abs(round(rec['rent'], 2)) if rec['rent'] < 0 else 0,
                            'credit': round(rec['rent'], 2) if rec['rent'] > 0 else 0
                        })
                    ])
        return lines

    @api.model
    def generate_sales_brand_entry(self):
        if not self.env.company.allow_sales_brand_entry:
            return
        start_date, end_date = self._get_sales_brand_entry_dates(self.env.company.sales_brand_entry_days)
        if not start_date or not end_date:
            return

        labels, lines = self._prepare_sales_brand_entry_lines(start_date, end_date)
        # Create sales brand entries group by journal
        for journal, label in labels.items():
            move_date = end_date.date()
            move_obj = self.env['account.move'].sudo()
            if move_obj.search_count([('ref', '=', f'{str(label)} Date: {str(move_date)}'), ('state', '!=', 'cancel')]):
                continue
            move_id = move_obj.with_context(check_move_validity=False).create({
                'ref': f'{str(label)} Date: {str(move_date)}',
                'move_type': 'entry',
                'is_sales_brand_entry': True,
                'journal_id': journal,
                'date': move_date,
                'line_ids': lines[journal]
            })
            # Confirm brand entries
            move_id.action_post()

    @api.model
    def generate_sales_rent_entry(self):
        if not self.env.company.allow_sales_brand_entry:
            return
        allow_run = self._get_sales_rent_entry_dates(self.env.company.sales_rent_entry_days)
        if not allow_run:
            return
        move_obj = self.env['account.move'].sudo()
        move_date = fields.Datetime.now().date()
        if move_obj.search_count([('ref', '=', f"Rent at {str(move_date)}"), ('state', '!=', 'cancel')]):
            return
        lines = self._prepare_sales_rent_entry_lines()
        if lines:
            # Create sales rent entry
            move_obj.with_context(check_move_validity=False).create({
                'ref': f"Rent at {str(move_date)}",
                'move_type': 'entry',
                'is_sales_rent_entry': True,
                'journal_id': self.env.company.sales_rent_journal_id.id,
                'line_ids': lines
            })


