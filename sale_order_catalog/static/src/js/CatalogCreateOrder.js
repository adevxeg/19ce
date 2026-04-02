/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { formView } from "@web/views/form/form_view";


class CatalogOrderWizardController extends formView.Controller {

    setup() {
        super.setup();
        this.action = useService("action");
    }

    async onRecordSaved(record) {
        await super.onRecordSaved(...arguments);
        const { partner_id, currency_id } = record.data;
        return this.action.doAction({
            type: "ir.actions.act_window_close",
            infos: {
                orderData: {
                    partner_id,
                    currency_id
                },
            },
        });
    }

}

registry.category("views").add("catalog_order_wizard_form", {
    ...formView,
    Controller: CatalogOrderWizardController,
});
