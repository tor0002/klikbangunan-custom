/** @odoo-module **/
/*
 * This file is used to restrict out of stock product from ordering and show restrict popup
 */
import Registries from 'point_of_sale.Registries';
import ProductScreen from 'point_of_sale.ProductScreen';
import { Gui } from 'point_of_sale.Gui';
import bus_service from "bus.BusService";
import session from "web.session";

const RestrictProductScreen = (ProductScreen) => class RestrictProductScreen extends ProductScreen {
    
    constructor() {
        super(...arguments);
        var bus_service_obj = bus_service.prototype;
        bus_service_obj["env"] = this.env;
        bus_service_obj.call("bus_service", "updateOption", "stock.pos", session.uid);
        bus_service_obj.call("bus_service", "onNotification", this, this._onNotification);
        bus_service_obj.call("bus_service", "startPolling");            
    }

    async _onNotification(notification){
        this._productQtyLongpolling()
    }

    mounted() {
        this._productQtyLongpolling();
        this.productQtyLongpolling = setInterval(this._productQtyLongpolling.bind(this), 5000);
    }

    willUnmount() {
        clearInterval(this.productQtyLongpolling);
    }    

    // async _productQtyLongpolling() {
    //     try {
    //         const result = await this.rpc({
    //             model: 'pos.config',
    //             method: 'get_product_qty',
    //             args: [this.env.pos.config.id],
    //         });
    //         result.forEach((product) => {
    //             const product_obj = this.env.pos.db.get_product_by_id(product.id);
    //             product_obj.q_product = product.quantity;
    //             console.log('Test', product_obj)
    //         });
    //         this.render();
    //     } catch (error) {
    //         if (error.message.code < 0) {
    //             await this.showPopup('OfflineErrorPopup', {
    //                 title: this.env._t('Offline'),
    //                 body: this.env._t('Unable to get product quantity'),
    //             });
    //         } else {
    //             throw error;
    //         }
    //     }
    // }

    // Ini dibuat untuk menghilangkan tampilan error
    async _productQtyLongpolling() {
        try {
            const result = await this.rpc({
                model: 'pos.config',
                method: 'get_product_qty',
                args: [this.env.pos.config.id],
            });
            result.forEach((product) => {
                const product_obj = this.env.pos.db.get_product_by_id(product.id);
                if (product_obj) {  // Pastikan produk tidak undefined
                    product_obj.q_product = product.quantity;
                    console.log('Test', product_obj);
                } else {
                    console.warn(`Product with id ${product.id} is not found in the POS database.`);
                }
            });
            this.render();
        } catch (error) {
            if (error.message.code < 0) {
                await this.showPopup('OfflineErrorPopup', {
                    title: this.env._t('Offline'),
                    body: this.env._t('Unable to get product quantity'),
                });
            } else {
                throw error;
            }
        }
    }
    


   _onNotification(notifications) {
       console.log('Test!')
       this.render(true);
   }    
    
    async _clickProduct(event) {
        // Overriding product item click to restrict product out of stock
        const product = event.detail;
        var type = this.env.pos.config.stock_type
        if (this.env.pos.config.is_restrict_product && ((type == 'qty_on_hand') && (product.qty_available <= 0)) | ((type == 'virtual_qty') && (product.virtual_available <= 0)) |
            ((product.qty_available <= 0) && (product.virtual_available <= 0))) {
            // If the product restriction is activated in the settings and quantity is out stock, it show the restrict popup.
            this.showPopup("RestrictStockPopup", {
                body: product.display_name,
                pro_id: product.id
            });
        }
        else{
            await super._clickProduct(event)
        }
    }

}
Registries.Component.extend(ProductScreen, RestrictProductScreen);
