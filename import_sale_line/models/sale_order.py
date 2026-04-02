from odoo import api, models, fields, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_import_line(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"].sudo()._for_xml_id(
            "import_sale_line.action_import_sale_line_view")
        action.update({
            "context": {'default_order_id': self.id}
        })
        return action
