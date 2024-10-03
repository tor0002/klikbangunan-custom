# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2017-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Further specifically customized by the workers of PT. Ismata Nusantara Abadi

{
    "name": "Purchase Stock Picking Return Invoicing",
    "summary": "Add an option to refund returned pickings",
    "version": "14.0.1.2.0",
    "category": "Purchases",
    "website": "https://github.com/OCA/account-invoicing",
    "author": "ForgeFlow, Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "development_status": "Mature",
    "depends": ["purchase_stock", "ksi_stock_kb", "ksi_return_reason"],
    "data": ["views/account_invoice_view.xml", "views/purchase_view.xml"],
    "maintainers": ["pedrobaeza", "MiquelRForgeFlow"],
}