from odoo import models, fields, api


class PivotReport(models.Model):
    _inherit = 'pivot.report'

    @api.model
    def _select_additional_sale_fields(self):
        select_additional_fields_ = super()._select_additional_sale_fields()
        select_additional_fields_.update({
            'season_id': 'so.season_id'
        })
        return select_additional_fields_

