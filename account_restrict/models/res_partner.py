from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_open_refunds(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'name': _('Refunds'),
            'context': {'create': False},
            'domain': [('move_type', 'in', ('in_refund', 'out_refund')), ('partner_id', '=', self.id)],
            'view_type': 'list',
            'view_mode': 'list,form',
            'target': 'current',
        }
