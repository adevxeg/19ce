from odoo import api, fields, models


class SalesBrand(models.Model):
    _name = 'sales.brand'
    _rec_name = 'name'
    _description = 'Sales Brand'

    name = fields.Char(string="Name", required=True)
    company_id = fields.Many2one(comodel_name="res.company", default=lambda self: self.env.company.id)
    type = fields.Selection(string="Type", selection=[('commission', 'Commission'), ('tax', 'Tax')], required=True)
    tax_id = fields.Many2one(comodel_name="account.tax", string="Tax", domain="[('type_tax_use', '=', 'sale')]")
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal", required=True)
    debit_account_id = fields.Many2one(comodel_name="account.account", string="Debit Account", required=True)
    credit_account_id = fields.Many2one(comodel_name="account.account", string="Credit Account", required=True)

    _type_unique = models.Constraint(
        'unique(company_id, type)', 'Sales Brand config type should be unique per company!')