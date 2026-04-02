from odoo.exceptions import UserError
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'variant.domain.abstract', 'template.domain.abstract']

    sales_type = fields.Selection(
        string="Sales Type", selection=[('sales', 'Sales'), ('credit_note', 'Credit Note')], default='sales')
    warehouse_id_domain = fields.Char(compute="_compute_warehouse_id_domain")

    def _calc_tmpl_domain_depends(self):
        res = super()._calc_tmpl_domain_depends()
        return res or ['order_id']

    def _calc_variant_domain_depends(self):
        res = super()._calc_variant_domain_depends()
        res.extend(['warehouse_id', 'partner_id', 'sales_type'])
        return res

    def _calc_variant_domain(self):
        if self.sales_type == 'credit_note':
            res = []
            _where = f"""WHERE (so.state = 'sale')"""
            if self.env.company.force_default_credit_note_warehouse:
                _where += f"  AND (so.warehouse_id = {self.warehouse_id.id if self.warehouse_id else 0})"
            if self.env.company.credit_note_by_customer:
                _where += f" AND (sol.order_partner_id = {self.partner_id.id if self.partner_id else 0})"
            self.env.cr.execute(""" 
                SELECT sol.product_id 
                FROM sale_order_line sol 
                    LEFT JOIN sale_order so ON (sol.order_id=so.id)
                """ + _where + """
            """)
            res.append(("id", "in", [row[0] for row in self.env.cr.fetchall()]))
            return res
        else:
            return super()._calc_variant_domain()


    def _default_warehouse_id(self):
        if self.env.user.restrict_sale_warehouse_by_user:
            if self.env.user.allowed_warehouse_ids:
                self.warehouse_id = self.env.user.allowed_warehouse_ids[0].id
        else:
            if self.sales_type == 'credit_note':
                self.warehouse_id = self.env.company.credit_note_warehouse_id.id
            else:
                self.warehouse_id = self.env.company.sale_warehouse_id.id

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            self._default_warehouse_id()
        super()._onchange_company_id()

    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.user_id:
            self.team_id = self.env['crm.team'].with_context(
                default_team_id=self.team_id.id)._get_default_team_id(user_id=self.user_id.id)
        if self.state in ['draft', 'sent'] and not self.warehouse_id:
            self._default_warehouse_id()

    @api.depends('create_uid', 'company_id')
    def _compute_warehouse_id_domain(self):
        for rec in self:
            domain = []
            if self.env.user.restrict_sale_warehouse_by_user:
                domain.append(('id', 'in', self.env.user.allowed_warehouse_ids.ids))
            rec.warehouse_id_domain = domain

    @api.depends('user_id', 'company_id')
    def _compute_warehouse_id(self):
        super()._compute_warehouse_id()
        for rec in self:
            rec._default_warehouse_id()

    @api.onchange('warehouse_id')
    def _onchange_warehouse_id(self):
        if self.env.company.force_default_sale_warehouse and self.sales_type == 'sales':
            if self.warehouse_id != self.env.company.sale_warehouse_id:
                raise UserError(_(f'Warehouse Must Be: {self.env.company.sale_warehouse_id.name}'))
        if self.env.company.force_default_credit_note_warehouse and self.sales_type == 'credit_note':
            if self.warehouse_id != self.env.company.credit_note_warehouse_id:
                raise UserError(_(f'Warehouse Must Be: {self.env.company.credit_note_warehouse_id.name}'))

    def _auto_confirm_one_step(self):
        if self.sales_type == 'credit_note':
            self._auto_confirm_picking()
            self._auto_confirm_invoice(final=True)
        else:
            super()._auto_confirm_one_step()

    def action_confirm(self):
        if self.sales_type == 'credit_note':
            # Validate qty sold
            if self.env.company.credit_note_validate_qty_sold:
                product_names = self.order_line.filtered(
                    lambda x: abs(x.product_uom_qty) > x.qty_sold and x.product_id.is_storable).mapped('product_id.name')
                if product_names:
                    raise UserError(_('Quantity must be less than or equal sold qty in %s' % product_names))
        return super(SaleOrder, self).action_confirm()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'sales_type' in vals and vals['sales_type'] == 'credit_note':
                if 'company_id' in vals:
                    self = self.with_company(vals['company_id'])
                if vals.get('name', _("New")) == _("New"):
                    seq_date = fields.Datetime.context_timestamp(
                        self, fields.Datetime.to_datetime(vals['date_order'])
                    ) if 'date_order' in vals else None
                    vals['name'] = self.env['ir.sequence'].next_by_code(
                        'sale.order.credit', sequence_date=seq_date) or _("New")

        return super().create(vals_list)
