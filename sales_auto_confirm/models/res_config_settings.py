from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    one_step_sale = fields.Boolean(related="company_id.one_step_sale", readonly=False)

