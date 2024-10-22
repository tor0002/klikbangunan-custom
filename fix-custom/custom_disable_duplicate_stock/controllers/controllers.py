# -*- coding: utf-8 -*-
# from odoo import http


# class CustomDisableDuplicateStock(http.Controller):
#     @http.route('/custom_disable_duplicate_stock/custom_disable_duplicate_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_disable_duplicate_stock/custom_disable_duplicate_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_disable_duplicate_stock.listing', {
#             'root': '/custom_disable_duplicate_stock/custom_disable_duplicate_stock',
#             'objects': http.request.env['custom_disable_duplicate_stock.custom_disable_duplicate_stock'].search([]),
#         })

#     @http.route('/custom_disable_duplicate_stock/custom_disable_duplicate_stock/objects/<model("custom_disable_duplicate_stock.custom_disable_duplicate_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_disable_duplicate_stock.object', {
#             'object': obj
#         })
