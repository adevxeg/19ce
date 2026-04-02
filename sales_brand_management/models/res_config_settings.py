from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_sales_brand_entry = fields.Boolean(related="company_id.allow_sales_brand_entry", readonly=False)
    sales_brand_ids = fields.One2many(related="company_id.sales_brand_ids", readonly=False)
    sales_brand_entry_days = fields.Char(related="company_id.sales_brand_entry_days", readonly=False)
    sales_rent_journal_id = fields.Many2one(related="company_id.sales_rent_journal_id", readonly=False)
    sales_rent_debit_account_id = fields.Many2one(related="company_id.sales_rent_debit_account_id", readonly=False)
    sales_rent_credit_account_id = fields.Many2one(related="company_id.sales_rent_credit_account_id", readonly=False)
    sales_rent_entry_days = fields.Char(related="company_id.sales_rent_entry_days", readonly=False)
    sales_brand_warehouse_restrict = fields.Boolean(related="company_id.sales_brand_warehouse_restrict", readonly=False)
    sales_warehouse_categ_restrict = fields.Boolean(related="company_id.sales_warehouse_categ_restrict", readonly=False)

    @api.onchange('sales_brand_entry_days')
    def onchange_sales_brand_entry_days(self):
        days = eval(self.sales_brand_entry_days)
        if not isinstance(days, list):
            raise ValidationError(_("Sales Brand Entry Days should be a list !!"))

    @api.onchange('sales_rent_entry_days')
    def onchange_sales_rent_entry_days(self):
        days = eval(self.sales_rent_entry_days)
        if not isinstance(days, list):
            raise ValidationError(_("Rent Entry Days should be a list !!"))
