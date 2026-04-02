from odoo import api, fields, models


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'season.abstract', 'variant.domain.abstract']

    def _calc_variant_domain_depends(self):
        res = super()._calc_variant_domain_depends()
        res.extend(['move_type', 'season_id'])
        return res

    def _calc_variant_domain(self):
        res = super()._calc_variant_domain()
        if self.env.user.has_group('base_season.group_allow_season') and self.env.company.bill_refund_by_season:
            if self.move_type in ['in_invoice', 'in_refund']:
                res.append(("season_id", "=", self.season_id.id))
        return res

