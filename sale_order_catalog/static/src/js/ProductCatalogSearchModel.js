/** @odoo-module **/

import { SearchModel } from "@web/search/search_model";


export class OrderProductCatalogSearchModel extends SearchModel {

    async load() {
        await super.load(...arguments);
        await this._loadWarehouses();
    }

    getWarehouses() {
        return this.warehouses;
    }

    async _loadWarehouses() {
        this.warehouses = await this.orm.call(
            'stock.warehouse',
            'get_current_warehouses',
            [[]],
            { context: this.context },
        );
    }

    async clearWarehouseContext() {
        delete this.globalContext.warehouse_id;
        await this._notify();

    }

    async applyWarehouseContext(warehouse_id) {
        this.globalContext['warehouse_id'] = warehouse_id;
        await this._notify();
    }

}
