odoo.define("sh_pos_order_sync.action_button", function (require) {
    "use strict";

    const rpc = require("web.rpc");
    const PosComponent = require("point_of_sale.PosComponent");
    const { useListener } = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const orderlist_action_button = require("sh_pos_order_list.action_button");

    const POSOrderSyncScreen = (orderlist_action_button) =>
        class extends orderlist_action_button {
            onClickOrderHistoryButton() {
                var self = this;
                const { confirmed, payload } = self.showTempScreen("OrderListScreen");
                if (confirmed) {
                }
            }
        };
    Registries.Component.extend(orderlist_action_button, POSOrderSyncScreen);

    class SendOrderButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener("click-send-order-button", this.onClickSendOrderButton);
        }
        async onClickSendOrderButton() {
        	var self = this;
            console.log("SendOrderButton :: ", this);
            console.log("env.pos.all_session ::", this.env.pos.all_session);
            if (this.env.pos.get_order().get_selected_orderline()) {
                console.log("SendOrderButton 1 :: ", this);
            	
            	await rpc.query({
                    model: "pos.session",
                    domain: ['|',["state", "=", "opened"], ["state", "=", "opening_control"]],
                    method: "search_read",
                }).then(function (all_session) {

                    console.log("SendOrderButton 2 :: ", this);
                    
                    self.env.pos.all_session = all_session;
                })

                console.log("SendOrderButton 3 :: ", this);
            	
                let { confirmed, payload } = this.showPopup("TemplateReceiverPopupWidget");
                console.log("SendOrderButton 4 :: ", this);
                if (confirmed) {
                } else {
                    console.log("SendOrderButton 5 :: ", this);
                    return;
                }
                console.log("SendOrderButton 6 :: ", this);
            } else {
                alert("Please select the product !");
            }
        }
    }
    SendOrderButton.template = "SendOrderButton";
    ProductScreen.addControlButton({
        component: SendOrderButton,
        condition: function () {
            console.log("this.env.pos.config.user_type :: ", this.env.pos.config.user_type);
            return this.env.pos.config.user_type == "send" || this.env.pos.config.user_type == "both";
        },
    });
    Registries.Component.add(SendOrderButton);

    class SaveOrderButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener("click-save-order-button", this.onClickSaveOrderButton);
        }
        onClickSaveOrderButton() {
            var self = this;
            if (self.env.pos.get_order().is_edit) {
                self.env.pos.push_orders(self.env.pos.get_order());
                self.env.pos.add_new_order();
                $(".save_button").removeClass("show_save_button");
            }
        }
    }
    SaveOrderButton.template = "SaveOrderButton";
    ProductScreen.addControlButton({
        component: SaveOrderButton,
        condition: function () {
            return true;
        },
    });
    Registries.Component.add(SaveOrderButton);
});
