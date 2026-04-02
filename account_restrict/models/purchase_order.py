from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _prepare_invoice(self):
        res = super(PurchaseOrder, self)._prepare_invoice()
        res['restrict_update_line_qty'] = True
        return res
