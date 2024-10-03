odoo.define('ksi_partner_kb.models', function (require){
    "use strict";

    const models = require('point_of_sale.models');

    models.load_fields('res.partner','alamat_pengiriman');

    // var existing_models = models.PosModel.prototype.models;
    // var product_index = _.findIndex(existing_models, function (model) {
    //     return model.model === "res.partner";
    // });
    // var product_model = existing_models[product_index];
    
    // models.load_models([{
    //     model:  product_model.model,
    //     label:  product_model.label,
    //     fields: ['name','street','city','state_id','country_id','vat','lang',
    //              'phone','zip','mobile','email','barcode','write_date',
    //              'property_account_position_id','property_product_pricelist','alamat_pengiriman'],
    //     domain: product_model.domain,
    //     loaded: product_model.loaded,
    // }]);

    // console.log("==========>>> PosModel prototype models", models.PosModel.prototype.models)
});