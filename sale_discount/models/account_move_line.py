from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_amount_discount(self):
        if self.product_id == self.env.company.sale_discount_product_id:
            return abs(self.quantity * self.price_unit)
        return super()._get_amount_discount()