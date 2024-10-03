odoo.define('pos_restrict_price.Orderline', function(require) {
    "use strict";
    
    const Orderline = require('point_of_sale.Orderline');
    const Registries = require('point_of_sale.Registries');
    const Gui = require('point_of_sale.Gui');
    
    const RestrictPriceOrderline = (Orderline) => class extends Orderline {
        set_unit_price(price) {
            const product = this.product;
            if (product && !product.is_price_within_range(price)) {
                Gui.showPopup('ErrorPopup', {
                    title: this.env._t('Price Restriction'),
                    body: this.env._t(`The price of ${product.display_name} must be between ${product.min_price} and ${product.max_price}.`),
                });
                return;  // Stop further execution if price is out of range
            }
            super.set_unit_price(price);
        }
    };
    
    Registries.Component.extend(Orderline, RestrictPriceOrderline);
    
    return RestrictPriceOrderline;
});
