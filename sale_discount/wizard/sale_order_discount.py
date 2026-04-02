from odoo.exceptions import ValidationError
from odoo import api, fields, models, Command, _


class SaleOrderDiscount(models.TransientModel):
    _inherit = 'sale.order.discount'

    def _get_discount_type_selection(self):
        shared_selection = [('sol_discount', "On All Order Lines"), ('so_discount', "Global Discount")]
        if self.env.company.sale_discount_type != 'adevx':
            return shared_selection + [('amount', "Fixed Amount")]
        else:
            return shared_selection

    discount_mode = fields.Selection([
        ('amount', 'Amount'), ('percentage', 'Percentage')
    ], string='Discount Mode', default='percentage')
    discount_type = fields.Selection(selection=_get_discount_type_selection, default='sol_discount')
    sale_discount_type = fields.Selection(related='sale_order_id.sale_discount_type')

    @api.constrains('discount_type', 'discount_percentage')
    def _check_discount_amount(self):
        if self.discount_mode == 'percentage':
            super()._check_discount_amount()
            for wizard in self:
                if wizard.discount_type in ('sol_discount', 'so_discount') and wizard.discount_percentage < 0.0:
                    raise ValidationError(_("Invalid discount amount"))
        else:
            for wizard in self:
                if (wizard.discount_amount < 0.0 or
                        (wizard.discount_type == 'so_discount' and wizard.discount_amount <= 0.0)):
                    raise ValidationError(_("Invalid discount amount"))

    @api.onchange('discount_type')
    def _onchange_discount_type(self):
        if self.sale_discount_type != 'adevx':
            if self.discount_type == 'amount':
                self.discount_mode = 'amount'
            else:
                self.discount_mode = 'percentage'

    def _prepare_discount_product_values(self):
        res = super()._prepare_discount_product_values()
        res['default_code'] = 'SO-DISCOUNT'
        return res

    def _create_discount_lines(self):
        # re-code this function to use discount mode
        self.ensure_one()
        self = self.with_context(lang=self.sale_order_id._get_lang())
        discount_product = self._get_discount_product()
        if self.discount_mode == 'percentage':
            amount_type = 'percent'
            amount = self.discount_percentage * 100.0
        else:
            amount_type = 'fixed'
            amount = self.discount_amount

        order = self.sale_order_id
        AccountTax = self.env['account.tax']
        order_lines = order.order_line.filtered(lambda x: not x.display_type and x.product_id != discount_product)
        base_lines = [line._prepare_base_line_for_taxes_computation() for line in order_lines]
        AccountTax._add_tax_details_in_base_lines(base_lines, order.company_id)
        AccountTax._round_base_lines_tax_details(base_lines, order.company_id)

        def grouping_function(base_line):
            return {'product_id': discount_product}

        global_discount_base_lines = AccountTax._prepare_global_discount_lines(
            base_lines=base_lines,
            company=self.company_id,
            amount_type=amount_type,
            amount=amount,
            computation_key=f'global_discount,{self.id}',
            grouping_function=grouping_function,
        )
        discount_lines = order.order_line.filtered(lambda l: l.product_id == discount_product)
        if discount_lines:
            discount_lines.unlink()
        order.order_line = [
            Command.create(values)
            for values in self._prepare_global_discount_so_lines(global_discount_base_lines)
        ]

    def action_apply_discount(self):
        if self.sale_discount_type != 'adevx':
            super().action_apply_discount()
        else:
            if self.discount_type == 'sol_discount':
                for line in self.sale_order_id.order_line.filtered(
                        lambda l: l.product_id != self._get_discount_product()):
                    total_price = line.product_uom_qty * line.price_unit
                    if self.discount_mode == 'percentage':
                        discount = self.discount_percentage * 100
                        amount_discount = total_price * self.discount_percentage
                    else:
                        discount = ((total_price - (total_price - self.discount_amount)) / total_price) * 100 or 0.0
                        amount_discount = self.discount_amount

                    if amount_discount > total_price:
                        raise ValidationError(_("Discount amount cannot be greater than total price"))
                    line.write({
                        'discount': discount,
                        'amount_discount': amount_discount
                    })
            else:
                super().action_apply_discount()