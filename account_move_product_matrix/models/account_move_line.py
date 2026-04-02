from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_template_id = fields.Many2one(
        comodel_name='product.template', string='Template', related="product_id.product_tmpl_id")
    product_tmpl_domain = fields.Char(related='move_id.product_tmpl_domain')
    is_configurable_product = fields.Boolean(
        string='Is the product configurable?', related="product_template_id.has_configurable_attributes")
    product_template_attribute_value_ids = fields.Many2many(
        related='product_id.product_template_attribute_value_ids', readonly=True)
    product_no_variant_attribute_value_ids = fields.Many2many(
        comodel_name='product.template.attribute.value', string='Product attribute values that do not create variants',
        ondelete='restrict')

    # =========================== Built-in functions =========================== #
    @api.depends('display_type')
    def _compute_quantity(self):
        for line in self:
            if not line.quantity:
                line.quantity = 1 if line.display_type == 'product' else False
