odoo.define('ksi_work_entry_contract_kb.ChangePassword', function (require) {
    "use strict";
    var WorkEntryControllerMixin = require('hr_work_entry_contract.WorkEntryControllerMixin');

    // ! disable automatic work entries
    WorkEntryControllerMixin._generateWorkEntries =  function () {
        var self = this;
        // return this._rpc({
        //     model: 'hr.employee',
        //     method: 'generate_work_entries',
        //     args: [[], time.date_to_str(this.firstDay), time.date_to_str(this.lastDay)],
        // }).then(function (new_work_entries) {
        //     if (new_work_entries) {
        //         self.reload();
        //     }
        // });
        return false
    }
});
    