/** @odoo-module **/

import ProductItem from "point_of_sale.ProductItem";
import Registries from "point_of_sale.Registries";
import bus_service from "bus.BusService";
import session from "web.session";

const StockProductsItem = (ProductItem) =>
    class extends ProductItem {

        get productQuantity() {
            const product = this.props.product;
            return product.q_product !== undefined
                ? product.q_product
                : this.env.pos.db.get_product_by_id(product.id).get_quantity();
        }            
    };

Registries.Component.extend(ProductItem, StockProductsItem);
