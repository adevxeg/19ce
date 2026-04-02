from odoo import fields, models, api


class PartnerWarehouse(models.Model):
    _name = 'partner.warehouse'
    _description = 'Partner Warehouse'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Warehouse', required=True)
    rent_amount = fields.Float(string='Rent Amount', required=True)
