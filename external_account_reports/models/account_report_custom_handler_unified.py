import xmlrpc.client
from odoo import models, api, fields
from odoo.tools import float_is_zero


class UnifiedReportHandler(models.AbstractModel):
    _name = 'account.report.custom.handler.unified'
    _inherit = 'account.report.custom.handler'
    _description = 'Unified Report Handler (Multi-Column)'

    def _custom_options_initializer(self, report, options, previous_options=None):
        super()._custom_options_initializer(report, options, previous_options)
        # 1. Check if the user has already interacted with this filter
        if previous_options and 'merge_external_db' in previous_options:
            # Carry over the user's choice (True or False)
            options['merge_external_db'] = previous_options['merge_external_db']
        else:
            # Default state for the very first time the report opens
            options['merge_external_db'] = False
        # 2. Update the 'extra_options' list for the UI Dropdown
        options.setdefault('extra_options', []).append({
            'id': 'merge_external_db',
            'name': 'merge_external_db',
            'label': 'Include External DB',
            'selected': options['merge_external_db'],  # Use the value we just set
        })
        # 3. Update the 'custom_display_config' to use our custom template
        options['custom_display_config'] = {
            'templates': {
                'AccountReportFilters': 'account_reports.ExternalDBFilters',
            },
        }

    def _custom_columns_initializer(self, report, options, columns):
        if options.get('merge_external_db'):
            columns.append({'name': 'External DB', 'class': 'number'})
            columns.append({'name': 'Grand Total', 'class': 'number'})
        return columns

    # --- 3. Inject Column Data (Cells) ---
    def _custom_line_postprocessor(self, report, options, lines):
        if options.get('merge_external_db'):
            external_map = self._fetch_external_data(options)
            currency = self.env.company.currency_id
            for line in lines:
                # 1. Identify if this is a data line or a section title
                # account.account lines have caret_options
                is_account_line = line.get('caret_options') == 'account.account'
                # 2. Get the values
                local_val = 0.0
                if is_account_line:
                    # Safely get the local balance from the first existing column
                    local_val = line['columns'][0].get('no_format', 0.0)
                    # Extract account code to match with external data
                    account_code = line.get('name', '').split(' ')[0]
                    external_val = external_map.get(account_code, 0.0)
                else:
                    # For section headers (like "Income"), we need to sum their children
                    # or leave as 0.0 if you handle totals separately.
                    external_val = 0.0  # Or logic to sum children

                total_val = local_val + external_val
                # Column: External DB
                line['columns'].append({
                    'name': currency.format(external_val) if is_account_line or external_val != 0 else '',
                    'no_format': external_val,
                    'class': 'number text-muted'
                })
                # Column: Grand Total
                line['columns'].append({
                    'name': currency.format(total_val) if is_account_line or total_val != 0 else '',
                    'no_format': total_val,
                    'class': 'number fw-bold'
                })
        return lines

    # --- 4. XML-RPC Fetcher (Same as before) ---
    def _fetch_external_data(self, options):
        """ Connects to DB2 and performs read_group """
        url = "http://192.168.100.10:8020"
        db = "V19EE_bavly"
        username = "admin"
        password = "nimda"

        try:
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            # Map Odoo Report Dates (from options) to DB2 domain
            date_from = options['date']['date_from']
            date_to = options['date']['date_to']
            domain = [
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('parent_state', '=', 'posted')
                # Add 'company_id' filter here if you only want C3/C4
            ]
            # Fetch Grouped Data
            groups = models.execute_kw(
                db, uid, password,
                'account.move.line',
                'read_group',
                [domain, ['account_id', 'balance'], ['account_id']]
            )
            # Transform to simpler dict { 'code': balance }
            result = {}
            for g in groups:
                account_id = g.get('account_id', [])
                if account_id:
                    # account_id is (ID, "Code Name")
                    code = account_id[1].split(' ')[0]
                    result[code] = g.get('balance')
            return result
        except Exception as e:
            return {}