from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_discount_type = fields.Selection(selection=[
        ('standard', 'Standard Discount'), ('adevx', 'Adevx Discount')
    ], string="Sale Discount Type", default='standard')
