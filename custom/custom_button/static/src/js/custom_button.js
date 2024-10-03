odoo.define("custom_button.CustomButton", function (){
"use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");

    class CustomButton extends PosComponent {

    }

    CustomButton.template = "CustomButton";
    ProductScreen.addControlButton({
        component: CustomButton,
        position: ["before", "OrderlineCustomerNoteButton"],
    });

    Registries.Component.add(CustomButton);
    return CustomButton;
});