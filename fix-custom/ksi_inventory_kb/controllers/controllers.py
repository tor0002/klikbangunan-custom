# -*- coding: utf-8 -*-
# from odoo import http


# class KsiInventoryKb(http.Controller):
#     @http.route('/ksi_inventory_kb/ksi_inventory_kb', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_inventory_kb/ksi_inventory_kb/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_inventory_kb.listing', {
#             'root': '/ksi_inventory_kb/ksi_inventory_kb',
#             'objects': http.request.env['ksi_inventory_kb.ksi_inventory_kb'].search([]),
#         })

#     @http.route('/ksi_inventory_kb/ksi_inventory_kb/objects/<model("ksi_inventory_kb.ksi_inventory_kb"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_inventory_kb.object', {
#             'object': obj
#         })
