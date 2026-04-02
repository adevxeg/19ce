from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    allow_sales_brand_entry = fields.Boolean(string="Allow Sales Brand Entry")
    sales_brand_ids = fields.One2many(comodel_name="sales.brand", inverse_name="company_id")
    sales_brand_entry_days = fields.Char(string="Sales Brand Entry Days", default="[1]")
    sales_rent_journal_id = fields.Many2one(comodel_name="account.journal", string="Journal")
    sales_rent_debit_account_id = fields.Many2one(comodel_name="account.account", string="Debit Account")
    sales_rent_credit_account_id = fields.Many2one(comodel_name="account.account", string="Credit Account")
    sales_rent_entry_days = fields.Char(string="Rent Entry Days", default="[1]")
    sales_brand_warehouse_restrict = fields.Boolean(string='Sales Brand Warehouse Restrict')
    sales_warehouse_categ_restrict = fields.Boolean(string='Sales Warehouse Category Restrict')
