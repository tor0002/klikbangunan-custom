odoo.define('ksi_report_kb.action_handler', function (require) {
"use strict";
/**
 * Button 'Create' is replaced by Custom Button 
**/

var core = require('web.core');
var ListController = require('web.ListController');
ListController.include({
   renderButtons: function($node) {
   this._super.apply(this, arguments);
       if (this.$buttons) {
         this.$buttons.find('.o_list_tender_button_create').click(this.proxy('action_def'));
       }
    },
      
    //--------------------------------------------------------------------------
    // Define Handler for new Custom Button
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {MouseEvent} event
     */
    action_def: function (e) {
        var self = this;
        var active_id = this.model.get(this.handle).getContext()['active_ids'];
        console.log(active_id);
        var model_name = this.model.get(this.handle).getContext()['active_model'];
        console.log(model_name);
            this._rpc({
                    model: 'ksi.report.kb.sale.transaction',
                    method: 'generate',
                    args: ["", model_name, active_id],
                }).then(function (result) {
                    self.do_action(result);
                });
   },
});
});