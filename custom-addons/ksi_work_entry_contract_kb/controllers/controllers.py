# -*- coding: utf-8 -*-
# from odoo import http


# class KsiWorkEntryContractKb(http.Controller):
#     @http.route('/ksi_work_entry_contract_kb/ksi_work_entry_contract_kb', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_work_entry_contract_kb/ksi_work_entry_contract_kb/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_work_entry_contract_kb.listing', {
#             'root': '/ksi_work_entry_contract_kb/ksi_work_entry_contract_kb',
#             'objects': http.request.env['ksi_work_entry_contract_kb.ksi_work_entry_contract_kb'].search([]),
#         })

#     @http.route('/ksi_work_entry_contract_kb/ksi_work_entry_contract_kb/objects/<model("ksi_work_entry_contract_kb.ksi_work_entry_contract_kb"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_work_entry_contract_kb.object', {
#             'object': obj
#         })
