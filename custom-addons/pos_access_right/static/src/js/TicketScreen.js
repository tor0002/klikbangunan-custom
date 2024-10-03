odoo.define("pos_access_right.TicketScreen", function (require) {
  "use strict";

  const Registries = require("point_of_sale.Registries");
  const TicketScreen = require("point_of_sale.TicketScreen");

  const PosTicketScreen = (TicketScreen) =>
    class extends TicketScreen {
      get hasNewOrdersControlRights() {
        if (this.env.pos.get_cashier().hasGroupMultiOrder) {
          return true;
        }
        return false;
      }

      async _onDeleteOrder(order) {
        if (this.env.pos.get_cashier().hasGroupDeleteOrder) {
          return super._onDeleteOrder(order);
        }
        return false;
      }

      get hasDeleteOrdersRights() {
        if (this.env.pos.get_cashier().hasGroupDeleteOrder) {
          return true;
        }
        return false;
      }
    };

  Registries.Component.extend(TicketScreen, PosTicketScreen);

  return TicketScreen;
});
