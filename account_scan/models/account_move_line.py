from odoo.exceptions import UserError
from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_variant_domain = fields.Char(related='move_id.product_variant_domain')

    def _check_product_validity(self):
        domain = self.move_id._calc_variant_domain()
        domain.append(("id", "=", self.product_id.id))
        product_id = self.env['product.product'].search(domain)
        if not product_id:
            raise UserError(_("Product exist in system but not in domain !!"))
