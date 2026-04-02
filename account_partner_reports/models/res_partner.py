from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # =========================== Action functions =========================== #
    def action_open_dynamic_pl(self):
        self.ensure_one()
        report = self.env.ref('account_reports.partner_ledger_report')
        return {
            'type': 'ir.actions.client',
            'tag': 'account_report',
            'name': _('Partner Ledger: %s') % self.name,
            'params': {
                'options': {
                    'partner_ids': [self.id],
                    'unfold_all': True,
                },
                'ignore_session': True
            },
            'context': {
                'report_id': report.id
            },
        }

    def action_open_journal_items(self):
        return {
            'name': _('Journal Items'),
            'view_mode': 'list',
            'res_model': 'account.move.line',
            'view_id': self.env.ref('account.view_move_line_tree').id,
            'type': 'ir.actions.act_window',
            'domain': [('partner_id', '=', self.id)],
        }