
odoo.define("pos_restrict_product_stock.models", function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    
    models.load_fields('product.product', ['qty_available','virtual_available']);
    
    var super_product = models.Product.prototype;
    models.Product = models.Product.extend({        

        get_quantity: function() {
            var self = this;
            var type = this.pos.config.stock_type
            var q_product = 0
            if (type == 'qty_on_hand') {
                q_product =+ self.qty_available;
            } else {
                q_product =+ self.virtual_available;
            }
            
            return q_product;
        },
    })        

});
