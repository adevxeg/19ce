from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    one_step_sale = fields.Boolean(string="Sales In One Step", tracking=True)
