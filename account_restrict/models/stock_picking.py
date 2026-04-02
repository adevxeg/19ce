from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    allow_return_scrap = fields.Boolean(compute="_compute_allow_return_scrap")

    @api.depends('state')
    def _compute_allow_return_scrap(self):
        for rec in self:
            if rec.state == "done" and not self.env.user.has_group('account_restrict.group_picking_return_scrap'):
                rec.allow_return_scrap = False
            else:
                rec.allow_return_scrap = True

    @api.onchange('partner_id')
    def _onchange_partner_id_restrict(self):
        if self.partner_id:
            # POS Order
            if self.pos_order_id and self.pos_order_id.partner_id != self.partner_id:
                raise UserError('Partner must be  %s' % self.pos_order_id.partner_id.name)
            # Sale Order
            if self.sale_id and self.sale_id.partner_id != self.partner_id:
                raise UserError('Partner must be  %s' % self.sale_id.partner_id.name)
            # Purchase Order
            purchase_orders = self.move_ids.mapped('purchase_line_id.order_id')
            if purchase_orders and purchase_orders.partner_id != self.partner_id:
                raise UserError('Partner must be  %s' % purchase_orders.partner_id.name)
