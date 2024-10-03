# -*- coding: utf-8 -*-
# from odoo import http


# class KsiPurchaseStock(http.Controller):
#     @http.route('/ksi_purchase_stock/ksi_purchase_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_purchase_stock/ksi_purchase_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_purchase_stock.listing', {
#             'root': '/ksi_purchase_stock/ksi_purchase_stock',
#             'objects': http.request.env['ksi_purchase_stock.ksi_purchase_stock'].search([]),
#         })

#     @http.route('/ksi_purchase_stock/ksi_purchase_stock/objects/<model("ksi_purchase_stock.ksi_purchase_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_purchase_stock.object', {
#             'object': obj
#         })
