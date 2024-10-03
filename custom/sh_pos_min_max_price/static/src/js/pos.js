odoo.define('sh_pos_min_max_price.pos', function (require) {
    'use strict';

    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { Gui } = require("point_of_sale.Gui");
    var models = require("point_of_sale.models");

    models.load_fields('product.product', ['pro_min_sale_price', 'pro_max_sale_price'])

    const PosProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            _onClickPay() {
                var self = this
                var is_price_not_between = false
                var is_add = true
                _.each(this.env.pos.users, function (user) {
                    if (user["id"] == self.env.pos.get_cashier().user_id[0]) {
                        if (user.groups_id.indexOf(self.env.pos.config.sh_enable_pos_product_price_confirm[0]) === -1) {
                            is_price_not_between = false
                        } else {
                            is_price_not_between = true
                        }
                    }
                });
                _.each(this.env.pos.get_order().get_orderlines(), function (each_orderline) {
                    if (is_price_not_between && each_orderline.product.pro_max_sale_price && each_orderline.product.pro_max_sale_price != 0) {
                        if ((each_orderline.price > each_orderline.product.pro_max_sale_price) || (each_orderline.price < each_orderline.product.pro_min_sale_price)) {
                            is_add = false
                            self.env.pos.get_order().select_orderline(each_orderline)
                        }
                    }
                })
                if (is_add) {
                    this.showScreen('PaymentScreen');
                } else {
                    Gui.showPopup('ErrorPopup', {
                        title: 'Tolong Cek Kembali Harganya',
                        body: 'Open Price Tidak Boleh Melebihi Harga Maksimum dan Minimum!!!.',
                    });
                }
            }

        }

    Registries.Component.extend(ProductScreen, PosProductScreen);

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        set_unit_price: function (price) {
            var is_add = true
            var self = this;
            var is_price_not_between = false
            _.each(this.pos.users, function (user) {
                if (user["id"] == self.pos.get_cashier().user_id[0]) {
                    if (user.groups_id.indexOf(self.pos.config.sh_enable_pos_product_price_confirm[0]) === -1) {
                        is_price_not_between = false
                    } else {
                        is_price_not_between = true
                    }
                }
            });


            if (is_price_not_between && this.product.pro_max_sale_price && this.product.pro_max_sale_price != 0) {
                if ((price > this.product.pro_max_sale_price) || (price < this.product.pro_min_sale_price) || (this.price > this.product.pro_max_sale_price) || (this.price < this.product.pro_min_sale_price)) {
                    is_add = false
                }
            }

            if (is_add) {
                _super_orderline.set_unit_price.call(this, price)
            } else {

                Gui.showPopup('ErrorPopup', {
                    title: 'Product Price Alert',
                    body: 'Sale Price Should be Between ' + this.product.pro_min_sale_price + '-' + + this.product.pro_max_sale_price,
                });
                _super_orderline.set_unit_price.call(this, price)
            }
        }
    });
});
