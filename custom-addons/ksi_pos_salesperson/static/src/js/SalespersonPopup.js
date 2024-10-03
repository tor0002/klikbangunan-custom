odoo.define('ksi_pos_salesperson.SalespersonPopup', function(require){
    'use strict';

    const Popup = require('point_of_sale.ConfirmPopup');
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');
    var core = require('web.core');
    var _t = core._t;

    class SalespersonPopup extends Popup {

        constructor() {
            super(...arguments);
        }

        cancel() {
            this.trigger('close-popup');
        }

        add_salesperson() {
            var self = this;
            var empid = $("#empID").val();
            var emp_id;
            $('#emp_list > option').each(function(){
                if($(this).attr("value") == empid ){
                   emp_id = $(this).attr("id");
                }
            });
            if (emp_id) {
                var emp = this.env.pos.employee_by_id[emp_id]
                var order = this.env.pos.get_order();
                var orderlines = order.get_orderlines();
                if (this.props.type == 'order') {
                    for(var i = 0; i < orderlines.length; i++){
                        if(orderlines[i] != undefined){
                            orderlines[i].set_line_user(emp);
                        }
                    }
                }
                if (this.props.type == 'line' && this.props.selectedLine) {
                    this.props.selectedLine.set_line_user(emp);
                }
                this.trigger('close-popup');
            }
        }
    };
    
    SalespersonPopup.template = 'SalespersonPopup';

    Registries.Component.add(SalespersonPopup);

    return SalespersonPopup;

});
