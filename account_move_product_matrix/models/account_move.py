import json
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'template.domain.abstract']

    report_grids = fields.Boolean(
        string="Print Variant Grids", default=True,
        help="If set, the matrix of configurable products will be shown on the report of this record.")
    grid_product_tmpl_id = fields.Many2one(
        'product.template', store=False, help="Technical field for product_matrix functionalities.")
    grid_update = fields.Boolean(
        default=False, store=False, help="Whether the grid field contains a new matrix to apply or not.")
    grid = fields.Char(
        store=False,
        help="Technical storage of grid. \nIf grid_update, will be loaded on the Account Move. \nIf not, represents the matrix to open.")

    # =========================== Onchange functions =========================== #
    @api.onchange('grid_product_tmpl_id')
    def _set_grid_up(self):
        if self.grid_product_tmpl_id:
            self.grid_update = False
            self.grid = json.dumps(self._get_matrix(self.grid_product_tmpl_id))

    @api.onchange('grid')
    def _apply_grid(self):
        if self.grid and self.grid_update:
            grid = json.loads(self.grid)
            product_template = self.env['product.template'].browse(grid['product_template_id'])
            product_ids = set()
            dirty_cells = grid['changes']
            Attrib = self.env['product.template.attribute.value']
            default_move_vals = {}
            for cell in dirty_cells:
                combination = Attrib.browse(cell['ptav_ids'])
                no_variant_attribute_values = combination - combination._without_no_variant_attributes()

                # create or find product variant from combination
                product = product_template._create_product_variant(combination)
                # TODO replace the check on product_id by a first check on the ptavs and pnavs?
                # and only create/require variant after no line has been found ???
                invoice_line = self.invoice_line_ids.filtered(
                    lambda line: (line._origin or line).product_id == product and (
                            line._origin or line).product_no_variant_attribute_value_ids._origin == no_variant_attribute_values)

                # if product variant already exist in account move line
                old_qty = sum(invoice_line.mapped('quantity'))
                qty = cell['qty']
                diff = qty - old_qty

                if not diff:
                    continue

                product_ids.add(product.id)

                if invoice_line:
                    if qty == 0:
                        if self.state == 'draft':
                            # Remove lines if qty was set to 0 in matrix
                            # only if invoice state = draft
                            self.invoice_line_ids -= invoice_line
                        else:
                            invoice_line.update({'quantity': 0.0})
                    else:
                        if len(invoice_line) > 1:
                            raise ValidationError(
                                _("You cannot change the quantity of a product present in multiple Moves."))
                        else:
                            invoice_line[0].quantity = qty
                else:
                    if not default_move_vals:
                        AccountMoveLine = self.env['account.move.line']
                        default_move_vals = AccountMoveLine.default_get(AccountMoveLine._fields.keys())
                    last_sequence = self.invoice_line_ids[-1:].sequence
                    if last_sequence:
                        default_move_vals['sequence'] = last_sequence
                    new_line = self.invoice_line_ids.new({
                        **default_move_vals,
                        'product_id': product.id,
                        'quantity': qty,
                        'display_type': 'product',
                        'product_no_variant_attribute_value_ids': no_variant_attribute_values.ids
                    })
                    self.invoice_line_ids += new_line
            if product_ids:
                for line in self.invoice_line_ids:
                    line._check_product_validity()
                    line._compute_price_unit()
                    line._compute_totals()

    # =========================== Process functions =========================== #
    def _get_matrix(self, product_template):
        def has_ptavs(line, sorted_attr_ids):
            ptav = line.product_template_attribute_value_ids.ids
            pnav = line.product_no_variant_attribute_value_ids.ids
            pav = pnav + ptav
            pav.sort()
            return pav == sorted_attr_ids
        matrix = product_template._get_template_matrix(
            company_id=self.company_id,
            currency_id=self.currency_id)
        if self.invoice_line_ids:
            lines = matrix['matrix']
            invoice_line = self.invoice_line_ids.filtered(lambda line: line.product_template_id == product_template)
            for line in lines:
                for cell in line:
                    if not cell.get('name', False):
                        line = invoice_line.filtered(lambda line: has_ptavs(line, cell['ptav_ids']))
                        if line:
                            cell.update({
                                'qty': sum(line.mapped('quantity'))
                            })
        return matrix

    def get_report_matrixes(self):
        """Reporting method."""
        matrixes = []
        if self.report_grids:
            grid_configured_templates = self.invoice_line_ids.filtered('is_configurable_product').product_template_id
            # TODO is configurable product and product_variant_count > 1
            # configurable products are only configured through the matrix in account move, so no need to check product_add_mode.
            for template in grid_configured_templates:
                if len(self.invoice_line_ids.filtered(lambda line: line.product_template_id == template)) > 1:
                    matrix = self._get_matrix(template)
                    matrix_data = []
                    for row in matrix['matrix']:
                        if any(column['qty'] != 0 for column in row[1:]):
                            matrix_data.append(row)
                    matrix['matrix'] = matrix_data
                    matrixes.append(matrix)
        return matrixes
