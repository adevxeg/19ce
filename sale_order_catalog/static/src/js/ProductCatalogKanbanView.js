/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { OrderProductCatalogSearchModel } from "./ProductCatalogSearchModel";
import { OrderProductCatalogSearchPanel } from "./ProductCatalogSearchPanel";
import { OrderProductCatalogKanbanModel } from "./ProductCatalogKanbanModel";
import { OrderProductCatalogKanbanController } from "./ProductCatalogKanbanController";
import { ProductCatalogKanbanRenderer } from "@product/product_catalog/kanban_renderer";


export const ProductCatalogKanbanView = {
    ...kanbanView,
    Controller: OrderProductCatalogKanbanController,
    Model: OrderProductCatalogKanbanModel,
    Renderer: ProductCatalogKanbanRenderer,
    SearchModel: OrderProductCatalogSearchModel,
    SearchPanel: OrderProductCatalogSearchPanel
};

registry.category("views").add("sale_kanban_catalog", ProductCatalogKanbanView);
