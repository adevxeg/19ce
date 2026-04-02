from odoo import api, fields, models


class CatalogOrderWizard(models.TransientModel):
    _name = 'catalog.order.wizard'
    _description = 'Catalog Order Wizard'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer', required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency', default=lambda self: self.env.company.currency_id, required=True)
