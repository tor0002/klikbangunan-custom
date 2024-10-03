odoo.define('ksi_report_kb.list_renderer', function (require) {
"use strict";

    var ListRenderer = require('web.ListRenderer');
    ListRenderer.include({
        init: function (parent, state, params) {
            this._super(parent, state, params);
            console.log(state.context)
            if ('hasSelectors' in state.context && !state.context.hasSelectors)
                this.hasSelectors = false;
        },
    });

});