from odoo.tools import SQL
from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    season_id = fields.Many2one(comodel_name="season.season", string="Season", readonly=True)
    _depends = {'account.move': ['season_id']}

    def _select(self) -> SQL:
        return SQL("%s, move.season_id as season_id",super()._select())
