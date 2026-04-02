/** @odoo-module **/

import { onMounted } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";


export class OrderProductCatalogKanbanController extends ProductCatalogKanbanController {

    setup() {
        super.setup();
        this.notification = useService('notification');
    }

    async _defineButtonContent() {
        if (!this.orderId){
            this.buttonString = _t("Back to Quotation");
        }else{
            await super._defineButtonContent(...arguments);
        }
    }

    async backToQuotation() {
        if (!this.orderId){
            let contextOrderId = 0;
            if (this.actionService && this.actionService.currentController) {
                 contextOrderId = this.actionService.currentController.action.context.product_catalog_order_id;
            }
            this.orderId = contextOrderId;
            if (!this.orderId){
                return this.notification.add(_t("Please Add Product First !!"), {
                    type: "danger",
                });
            }
        }
        this.actionService.currentController.action.context.product_catalog_order_id = 0;
        return await super.backToQuotation(...arguments);
    }

}
