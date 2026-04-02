/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { onMounted, onPatched, onWillRender } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";


patch(ProductCatalogKanbanRecord.prototype, {

     setup() {
        super.setup();
        onWillRender(() => {
            this._ensureProductCatalogData();
        });
        onMounted(async () => {
            await this._updateQuantity(0);
        });
    },

    _ensureProductCatalogData() {
        if (this.props?.record && !this.props.record.productCatalogData) {
            this.props.record.productCatalogData = {
                quantity: 0,
                price: 0,
                uomDisplayName: "",
                readOnly: false
            };
        }
    },

    _getUpdateQuantityAndGetPriceParams() {
        this._ensureProductCatalogData();
        const catalogData = this.productCatalogData;
        const params = {
            order_id: this.env.orderId,
            product_id: this.env.productId,
            quantity: catalogData.quantity || 0,
            res_model: this.env.orderResModel,
            child_field: this.env.childField,
        };

        if (!params.order_id && this.action && this.action.currentController && this.action.currentController.action.context.product_catalog_order_id) {
            params.order_id = this.action.currentController.action.context.product_catalog_order_id;
        }
        return params;
    },

    updateQuantity(quantity) {
        this._ensureProductCatalogData();
        const catalogData = this.productCatalogData;
        if (catalogData.readOnly) {
            return;
        }
        catalogData.quantity = quantity || 0;
        this.debouncedUpdateQuantity();
    },

    addProduct(qty=1) {
        if (!this.action.currentController.action.context.product_catalog_order_id){
            let self = this;
            self.action.doAction(
                {
                    type: "ir.actions.act_window",
                    target: "new",
                    name: _t("Create New Order"),
                    res_model: "catalog.order.wizard",
                    views: [[false, "form"]],
                    context: {
                        catalog_res_model: self.env.orderResModel,
                    }
                },
                {
                    onClose: async (closeInfo) => {
                        if (closeInfo && closeInfo.orderData) {
                            const orderId = await self.orm.call(
                                self.env.orderResModel,
                                'create',
                                [{
                                    partner_id: closeInfo.orderData.partner_id.id,
                                    currency_id: closeInfo.orderData.currency_id.id
                                }]
                            );
                            // update context fields
                            self.action.currentController.action.context.product_catalog_order_id = orderId
                            self.action.currentController.action.context.product_catalog_currency_id = closeInfo.orderData.currency_id.id
                            self.updateQuantity(qty);
                        }
                    }
                }
            )
        } else {
            this.updateQuantity(qty);
        }
    }

});