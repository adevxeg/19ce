from odoo import api, fields, models, _


class AccountMoveDiscount(models.TransientModel):
    _inherit = 'account.move.discount'

    def _get_discount_product(self):
        sale_orders = self.move_id.invoice_line_ids.sale_line_ids.order_id
        if sale_orders:
            return self.env.company.sale_discount_product_id
        return super()._get_discount_product()