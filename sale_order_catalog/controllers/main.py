from odoo.http import request, route
from odoo.addons.product.controllers.catalog import ProductCatalogController


class OrderCatalogController(ProductCatalogController):

    @route()
    def product_catalog_get_order_lines_info(self, res_model, product_ids, order_id=False, **kwargs):
        if order_id:
            return super().product_catalog_get_order_lines_info(
                res_model=res_model, product_ids=product_ids, order_id=order_id, kwargs=kwargs)
        else:
            order_line_info = {}
            products = request.env['product.product'].browse(product_ids)
            for product in products:
                order_line_info[product.id] = {
                    'quantity': 0,
                    'deliveredQty': 0,
                    'price': product.lst_price,
                    'readOnly': False,
                    'uomDisplayName': ''
                }
            return order_line_info
