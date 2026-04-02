from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    journal_dashboard_balance = fields.Selection(
        string="Journal Dashboard Balance", required=True, default='journal',
        selection=[('standard', 'Standard'), ('journal', 'Journal'), ('account', 'Journal (Account)')])