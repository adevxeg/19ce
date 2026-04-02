from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    credit_note_by_customer = fields.Boolean(related="company_id.credit_note_by_customer", readonly=False)
    credit_note_validate_qty_sold = fields.Boolean(related="company_id.credit_note_validate_qty_sold", readonly=False)
    sale_warehouse_id = fields.Many2one(related="company_id.sale_warehouse_id", readonly=False)
    force_default_sale_warehouse = fields.Boolean(related="company_id.force_default_sale_warehouse", readonly=False)
    credit_note_warehouse_id = fields.Many2one(related="company_id.credit_note_warehouse_id", readonly=False)
    force_default_credit_note_warehouse = fields.Boolean(
        related="company_id.force_default_credit_note_warehouse", readonly=False)


