from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    account_discount_product_id = fields.Many2one(
        comodel_name='product.product', string="Account Discount Product",
        domain=[('type', '=', 'service'), ('invoice_policy', '=', 'order')],
        help="Default product used for discounts", check_company=True)
    account_discount_type = fields.Selection(selection=[
        ('standard', 'Standard Discount'), ('adevx', 'Adevx Discount')
    ], string="Account Discount Type", default='standard')
