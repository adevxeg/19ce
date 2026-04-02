from odoo import models, api, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    # =========================== Built-in functions =========================== #
    def _get_journal_dashboard_bank_running_balance(self):
        if self.env.context.get('journal_dashboard_balance'):
            if self.env.context.get('journal_dashboard_balance') == 'journal':
                return self._get_journal_dashboard_bank_running_balance_by_id()
            elif self.env.context.get('journal_dashboard_balance') == 'account':
                return self._get_journal_dashboard_bank_running_balance_by_account()
        else:
            if self.env.company.journal_dashboard_balance == 'journal':
                return self._get_journal_dashboard_bank_running_balance_by_id()
            elif self.env.company.journal_dashboard_balance == 'account':
                return self._get_journal_dashboard_bank_running_balance_by_account()

        return super()._get_journal_dashboard_bank_running_balance()

    # =========================== Customized functions =========================== #
    def _get_journal_dashboard_bank_running_balance_by_id(self):
        self.env.cr.execute("""
            SELECT 
                aj.id AS journal_id,
                COALESCE(SUM(aml.balance), 0) AS balance_end_real
            FROM account_move_line aml
                LEFT JOIN account_move am ON aml.move_id = am.id
                LEFT JOIN account_journal aj ON aml.journal_id = aj.id
            WHERE aj.id = ANY(%s)
                AND aml.account_id = aj.default_account_id
                AND aml.parent_state != 'cancel'
                AND am.origin_payment_id IS NULL
                AND aml.company_id = ANY(%s)
            GROUP BY 
                aj.id
        """, [self.ids, self.env.companies.ids])
        query_res = {res['journal_id']: res for res in self.env.cr.dictfetchall()}
        result = {}
        for journal in self:
            journal_vals = query_res.get(journal.id, {'balance_end_real': 0.0})
            result[journal.id] = (
                True if journal_vals['balance_end_real'] else False,
                journal_vals['balance_end_real'],
            )
        return result

    def _get_journal_dashboard_bank_running_balance_by_account(self):
        result = {}
        for journal in self:
            self.env.cr.execute("""
                SELECT 
                    COALESCE(SUM(aml.balance), 0) AS balance_end_real
                FROM account_move_line aml
                    LEFT JOIN account_move am ON aml.move_id = am.id
                WHERE aml.account_id = ANY(%s)
                    AND aml.parent_state != 'cancel'
                    AND am.origin_payment_id IS NULL
                    AND aml.company_id = ANY(%s)
            """, [journal.default_account_id.ids, self.env.companies.ids])
            query_res = {journal.id: res for res in self.env.cr.dictfetchall()}
            journal_vals = query_res.get(journal.id, {'balance_end_real': 0.0})
            result[journal.id] = (
                True if journal_vals['balance_end_real'] else False,
                journal_vals['balance_end_real'],
            )
        return result
