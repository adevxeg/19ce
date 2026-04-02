from odoo.tools import float_repr
from odoo.exceptions import ValidationError
from odoo import api, fields, models, Command, _


class AccountMoveDiscount(models.TransientModel):
    _name = 'account.move.discount'
    _description = "Discount Wizard"
    
    def _get_discount_type_selection(self):
        shared_selection = [('aml_discount', "On All Order Lines"), ('am_discount', "Global Discount")]
        if self.env.company.account_discount_type != 'adevx':
            return shared_selection + [('amount', "Fixed Amount")]
        else:
            return shared_selection

    move_id = fields.Many2one(
        'account.move', default=lambda self: self.env.context.get('active_id'), required=True)
    company_id = fields.Many2one(related='move_id.company_id')
    currency_id = fields.Many2one(related='move_id.currency_id')
    discount_amount = fields.Monetary(string="Amount")
    discount_percentage = fields.Float(string="Percentage")
    discount_type = fields.Selection(selection=_get_discount_type_selection, default='aml_discount')
    discount_mode = fields.Selection([
        ('amount', 'Amount'), ('percentage', 'Percentage')
    ], string='Discount Mode', default='percentage')
    account_discount_type = fields.Selection(related='move_id.account_discount_type')

    @api.constrains('discount_type', 'discount_percentage')
    def _check_discount_amount(self):
        for wizard in self:
            if wizard.discount_mode == 'percentage':
                if wizard.discount_type in ('aml_discount', 'am_discount') and wizard.discount_percentage > 1.0:
                    raise ValidationError(_("Invalid discount amount"))
                elif wizard.discount_type in ('aml_discount', 'am_discount') and wizard.discount_percentage < 0.0:
                    raise ValidationError(_("Invalid discount amount"))
            else:
                if (wizard.discount_amount < 0.0 or
                        (wizard.discount_type == 'am_discount' and wizard.discount_amount <= 0.0)):
                    raise ValidationError(_("Invalid discount amount"))

    @api.onchange('discount_type')
    def _onchange_discount_type(self):
        if self.account_discount_type != 'adevx':
            if self.discount_type == 'amount':
                self.discount_mode = 'amount'
            else:
                self.discount_mode = 'percentage'

    def _prepare_discount_product_values(self):
        self.ensure_one()
        values = {
            'name': _('Discount'),
            'type': 'service',
            'default_code': 'ACC-DISCOUNT',
            'invoice_policy': 'order',
            'list_price': 0.0,
            'company_id': self.company_id.id,
            'taxes_id': None,
        }
        services_category = self.env.ref('product.product_category_services', raise_if_not_found=False)
        if services_category:
            values['categ_id'] = services_category.id
        return values

    def _prepare_global_discount_am_lines(self, base_lines):
        self.ensure_one()
        discount_dp = self.env['decimal.precision'].precision_get('Discount')
        has_multiple_tax_combinations = len(
            set(base_line['tax_ids'] for base_line in base_lines if base_line['tax_ids'])) > 1
        am_line_values_list = []
        for base_line in base_lines:
            # The name of the po line.
            if has_multiple_tax_combinations:
                if self.discount_type == 'am_discount':
                    am_line_description = self.env._(
                        "Discount %(percent)s%%"
                        "- On products with the following taxes %(taxes)s",
                        percent=float_repr(self.discount_percentage * 100.0, discount_dp),
                        taxes=", ".join(base_line['tax_ids'].mapped('name')),
                    )
                else:
                    am_line_description = self.env._(
                        "Discount"
                        "- On products with the following taxes %(taxes)s",
                        taxes=", ".join(base_line['tax_ids'].mapped('name')),
                    )
            else:
                if self.discount_type == 'am_discount':
                    am_line_description = self.env._(
                        "Discount %(percent)s%%",
                        percent=float_repr(self.discount_percentage * 100.0, discount_dp),
                    )
                else:
                    am_line_description = self.env._("Discount")

            am_line_values_list.append({
                'name': am_line_description,
                'product_id': base_line['product_id'].id,
                'price_unit': base_line['price_unit'],
                'quantity': base_line['quantity'],
                'tax_ids': [Command.set(base_line['tax_ids'].ids)],
                'sequence': 999,
            })

        return am_line_values_list

    def _get_discount_product(self):
        """Return product.product used for discount line"""
        self.ensure_one()
        company = self.company_id
        discount_product = company.account_discount_product_id
        if not discount_product:
            if (
                    self.env['product.product'].has_access('create')
                    and company.has_access('write')
                    and company._has_field_access(company._fields['account_discount_product_id'], 'write')
            ):
                company.account_discount_product_id = self.env['product.product'].create(
                    self._prepare_discount_product_values()
                )
            else:
                raise ValidationError(_(
                    "There does not seem to be any discount product configured for this company yet."
                    " You can either use a per-line discount, or ask an administrator to grant the"
                    " discount the first time."
                ))
            discount_product = company.account_discount_product_id
        return discount_product

    def _create_discount_lines(self):
        self.ensure_one()
        self = self.with_context(lang=self.move_id._get_lang())
        discount_product = self._get_discount_product()
        if self.discount_mode == 'percentage':
            amount_type = 'percent'
            amount = self.discount_percentage * 100.0
        else:
            amount_type = 'fixed'
            amount = self.discount_amount

        order = self.move_id
        AccountTax = self.env['account.tax']
        invoice_lines = order.invoice_line_ids.filtered(
            lambda x: x.display_type == 'product' and x.product_id != discount_product)
        base_lines = [line.move_id._prepare_product_base_line_for_taxes_computation(line) for line in invoice_lines]
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
        discount_lines = order.invoice_line_ids.filtered(lambda l: l.product_id == discount_product)
        if discount_lines:
            discount_lines.unlink()
        order.invoice_line_ids = [
            Command.create(values)
            for values in self._prepare_global_discount_am_lines(global_discount_base_lines)
        ]

    def action_apply_discount(self):
        self.ensure_one()
        self = self.with_company(self.company_id)
        if self.discount_type == 'aml_discount':
            if self.account_discount_type != 'adevx':
                self.move_id.invoice_line_ids.write({'discount': self.discount_percentage * 100})
            else:
                for line in self.move_id.invoice_line_ids.filtered(
                        lambda l: l.product_id != self._get_discount_product()):
                    total_price = line.quantity * line.price_unit
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
            self._create_discount_lines()