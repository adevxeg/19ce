from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    bill_refund_by_season = fields.Boolean(string="Bill & Refund By Season", tracking=True)
