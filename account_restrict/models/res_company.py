from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    credit_note_by_customer = fields.Boolean(string="Credit Note By Customer")
    allow_credit_note_validate_sold_qty = fields.Boolean(string="Credit Note Validate Sold Qty")
    restrict_journal_negative_balance = fields.Boolean(string="Restrict Journal (cash, bank) Negative Balance")
