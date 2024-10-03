odoo.define('customer_deposit.customer_deposit', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var gui = require('point_of_sale.gui');
var models = require('point_of_sale.models');
var core = require('web.core');

var QWeb = core.qweb;
var _t = core._t;

models.load_fields('res.partner',['deposit_amount','amount_deposit']);
models.load_fields('pos.payment.method','is_deposit');


screens.PaymentScreenWidget.include({
    customer_changed: function() {
        var client = this.pos.get_client();
        this.$('.js_customer_name').text( client ? client.name : _t('Customer') );
        this.$('.js_customer_deposit').text( client ? client.amount_deposit : _t('Customer') );        
    },    
    click_paymentmethods : function(id) {
        var payment_method = this.pos.payment_methods_by_id[id];
        var order = this.pos.get_order();
        var client = this.pos.get_client();
        if (payment_method.is_deposit == true){
            var due = order.get_due();
            if (!client) {
                    var self = this;
                    this.gui.show_popup('confirm',{
                        'title': _t('Please select the Customer'),
                        'body': _t('You need to select the customer before you can invoice an order.'),
                        confirm: function(){
                            self.gui.show_screen('clientlist');
                        },
                    });
            } else {
                var deposit = client.amount_deposit;
                if ((deposit - due) < 0) {
                    this.gui.show_popup('error',{
                        'title': _t('Not Enough Deposit'),
                        'body':  _t('Customer Deposit Not Enough.'),
                    });
                } else {
                    this._super(id);
                }
            }
        } else {
            this._super(id);
        }
    }
});

});