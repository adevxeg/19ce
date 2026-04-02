from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SalesBrandReportWizard(models.TransientModel):
    _name = "sales.brand.report.wizard"
    _description = "Sales Brand Report Wizard"

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    partner_ids = fields.Many2many(comodel_name="res.partner", string="Partners", domain="[('sales_perc', '>', 0)]")
    type = fields.Selection(selection=[
        ('specific', 'Specific'), ('next', 'Next Entry Details')
    ], string='Type', default='specific', required=True)

    @api.onchange('start_date', 'end_date')
    def onchange_dates(self):
        if self.start_date and self.end_date and (self.start_date > self.end_date):
            raise ValidationError(_("Start Date must be before End Date !"))
        if self.start_date and not self.end_date:
            self.end_date = self.start_date + relativedelta(months=1)
        if self.end_date and not self.start_date:
            self.start_date = self.end_date - relativedelta(months=1)

    @api.onchange('type')
    def _onchange_type(self):
        if self.type == 'next':
            scheduled_days = eval(self.env.company.sales_brand_entry_days)
            last_commission_date = self.env['account.move'].search([
                ('is_sales_brand_entry', '=', True), ('state', '!=', 'cancel')], order='date desc', limit=1).date
            if not last_commission_date:
                last_commission_date = fields.Date.today()

            # Calculate start day index
            start_day_index = 0
            if last_commission_date.day:
                index = next((i for i, x in enumerate(scheduled_days) if x > last_commission_date.day), -1)
                start_day_index = index if index != -1 else 0
            # Calculate start date
            start_day = scheduled_days[start_day_index]
            if start_day < last_commission_date.day:
                next_month = last_commission_date + relativedelta(months=1)
                start_date = next_month.replace(day=start_day)
            else:
                start_date = last_commission_date.replace(day=start_day)
            # Calculate end date
            end_day = scheduled_days[start_day_index + 1] if start_day_index < len(scheduled_days) - 1 else \
            scheduled_days[0]
            if end_day <= start_day:
                next_month = start_date + relativedelta(months=1)
                end_date = next_month.replace(day=end_day)
            else:
                end_date = start_date.replace(day=end_day)

            self.start_date = start_date
            self.end_date = end_date

    def action_preview(self):
        if not self.env.company.allow_sales_brand_entry:
            raise ValidationError(_("Sales Brand Entry is not allowed for active company!"))
        # Get time from cron
        if self.type == 'next':
            brand_entry_cron = self.env.ref('sales_brand_management.cron_sales_brand_entry')
            start_date = datetime.combine(self.start_date, brand_entry_cron.nextcall.time())
            end_date = datetime.combine(self.end_date, brand_entry_cron.nextcall.time())
        else:
            start_date = self.start_date
            end_date = self.end_date

        partner_ids = self.partner_ids or self.env['res.partner'].search([('sales_perc', '>', 0)])
        return self.env["sales.brand.report"].view_report_details({
            'start_date': start_date,
            'end_date': end_date,
            'partner_ids': partner_ids.ids,
            'partner_names': ",".join(partner_ids.mapped("name")) if self.partner_ids else "All Partners"
        })
