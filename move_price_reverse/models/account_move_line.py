from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    allow_reverse_calc = fields.Boolean(compute="_compute_allow_reverse_calc")

    # =========================== Onchange functions =========================== #
    @api.onchange('price_total')
    def _onchange_price_total(self):
        taxes_amount = sum(self.tax_ids.mapped('amount'))
        if self.price_total and self.allow_reverse_calc:
            perc = (len(self.tax_ids) + (taxes_amount / 100))
            if perc and self.quantity:
                self.price_unit = self.price_total / perc / self.quantity

    # =========================== Compute functions =========================== #
    @api.depends('company_id', 'move_id.move_type')
    def _compute_allow_reverse_calc(self):
        for rec in self:
            if self.env.user.company_id.invoice_reverse_calc and rec.move_id.move_type == "out_invoice":
                rec.allow_reverse_calc = True
            else:
                rec.allow_reverse_calc = False

    def _compute_price_unit(self):
        for rec in self:
            if rec.move_id.move_type == 'out_refund' and rec.move_id.partner_id \
                    and rec.move_id.partner_id.property_product_pricelist and rec.product_id:
                price = rec.move_id.partner_id.property_product_pricelist._get_products_price(
                    rec.product_id, rec.quantity or 1.0, rec.move_id.partner_id)
                return price
        return super(AccountMoveLine, self)._compute_price_unit()
