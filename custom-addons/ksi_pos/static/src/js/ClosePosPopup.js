odoo.define("ksi_pos.ClosePosPopup", function (require) {
  "use strict";

  const Registries = require("point_of_sale.Registries");
  const ClosePosPopup = require("point_of_sale.ClosePosPopup");

  const PosClosePosPopup = (ClosePosPopup) =>
    class extends ClosePosPopup {
      // ! Overloading, change acceptClosing
      async willStart() {
        try {
          const closingData = await this.rpc({
            model: "pos.session",
            method: "get_closing_control_data",
            args: [[this.env.pos.pos_session.id]],
          });
          this.ordersDetails = closingData.orders_details;
          this.paymentsAmount = closingData.payments_amount;
          this.payLaterAmount = closingData.pay_later_amount;
          this.openingNotes = closingData.opening_notes;
          this.defaultCashDetails = closingData.default_cash_details;
          this.otherPaymentMethods = closingData.other_payment_methods;
          this.isManager = closingData.is_manager;
          this.amountAuthorizedDiff = closingData.amount_authorized_diff;

          // component state and refs definition
          //! Ganti acceptClosing:true by default
          const state = { notes: "", acceptClosing: true, payments: {} };
          // console.log("dari default", state);
          // state.acceptClosing = true;

          if (this.cashControl) {
            state.payments[this.defaultCashDetails.id] = {
              counted: 0,
              difference: -this.defaultCashDetails.amount,
              number: 0,
            };
          }
          if (this.otherPaymentMethods.length > 0) {
            this.otherPaymentMethods.forEach((pm) => {
              if (pm.type === "bank") {
                state.payments[pm.id] = {
                  counted: this.env.pos.round_decimals_currency(pm.amount),
                  difference: 0,
                  number: pm.number,
                };
              }
            });
          }
          Object.assign(this.state, state);
        } catch (error) {
          this.error = error;
        }
      }

      // ! Overloading disable ganti state acceptclosing
      handleInputChange(paymentId) {
        let expectedAmount;
        if (paymentId === this.defaultCashDetails.id) {
          this.manualInputCashCount = true;
          this.state.notes = "";
          expectedAmount = this.defaultCashDetails.amount;
        } else {
          expectedAmount = this.otherPaymentMethods.find(
            (pm) => paymentId === pm.id
          ).amount;
        }
        this.state.payments[paymentId].difference =
          this.env.pos.round_decimals_currency(
            this.state.payments[paymentId].counted - expectedAmount
          );
        // this.state.acceptClosing = false;
      }

      // ! Overloading disable ganti state acceptclosing
      updateCountedCash(event) {
        const { total, moneyDetailsNotes, moneyDetails } = event.detail;
        this.state.payments[this.defaultCashDetails.id].counted = total;
        this.state.payments[this.defaultCashDetails.id].difference =
          this.env.pos.round_decimals_currency(
            this.state.payments[[this.defaultCashDetails.id]].counted -
              this.defaultCashDetails.amount
          );
        if (moneyDetailsNotes) {
          this.state.notes = moneyDetailsNotes;
        }
        this.manualInputCashCount = false;
        this.moneyDetails = moneyDetails;
        // this.state.acceptClosing = false;
      }
    };

  Registries.Component.extend(ClosePosPopup, PosClosePosPopup);

  return ClosePosPopup;
});
