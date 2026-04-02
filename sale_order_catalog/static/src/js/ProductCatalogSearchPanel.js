/** @odoo-module **/

import { SearchPanel } from "@web/search/search_panel/search_panel";


export class OrderProductCatalogSearchPanel extends SearchPanel {
    setup() {
        super.setup();
        this.selectedWarehouse = null;
    }

    get warehouses() {
        return this.env.searchModel.getWarehouses() || [];
    }

    clearWarehouseContext() {
        this.env.searchModel.clearWarehouseContext();
        this.selectedWarehouse = null;
    }

    applyWarehouseContext(warehouse_id) {
        this.env.searchModel.applyWarehouseContext(warehouse_id);
        this.selectedWarehouse = warehouse_id;
    }

}

OrderProductCatalogSearchPanel.template = "ProductCatalogSearchPanel";
