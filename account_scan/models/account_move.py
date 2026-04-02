from odoo.exceptions import UserError
from odoo import api, models, fields, _


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ['account.move', 'variant.domain.abstract']

    barcode = fields.Char(string='Barcode')

    def _calc_variant_domain(self):
        res = super()._calc_variant_domain()
        res.extend(['|', ('sale_ok', '=', True), ('purchase_ok', '=', True)])
        return res

    @api.onchange('barcode')
    def onchange_barcode(self):
        if self.barcode:
            domain = []
            if self.env.user.company_id.scan_type == 'barcode':
                domain.append(('barcode', '=', self.barcode))
            elif self.env.user.company_id.scan_type == 'code':
                domain.append(('default_code', '=', self.barcode))
            else:
                raise UserError(_('Unknown Company Scan Type !!'))

            product_id = self.env['product.product'].search(domain, limit=1)
            if not product_id:
                if self.env.user.company_id.scan_type == 'barcode':
                    raise UserError(_("Unknown Barcode: %s !!" % str(self.barcode)))
                elif self.env.user.company_id.scan_type == 'code':
                    raise UserError(_("Unknown Default Code: %s !!" % str(self.barcode)))

            if any(line for line in self.invoice_line_ids if line.product_id.id == product_id.id):
                move_line = self.invoice_line_ids.filtered(lambda l: l.product_id.id == product_id.id)
                move_line[0]._check_product_validity()
                move_line[0].quantity = move_line[0].quantity + 1.0
                move_line[0]._compute_totals()
            else:
                new_line = self.invoice_line_ids.new({
                    'product_id': product_id.id,
                    'quantity': 1
                })
                self.invoice_line_ids += new_line
                for line in self.invoice_line_ids:
                    line._check_product_validity()
                    line._compute_price_unit()
                    line._compute_totals()
            self.barcode = ""
