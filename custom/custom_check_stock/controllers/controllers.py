# -*- coding: utf-8 -*-
# from odoo import http


# class CustomCheckStock(http.Controller):
#     @http.route('/custom_check_stock/custom_check_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_check_stock/custom_check_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_check_stock.listing', {
#             'root': '/custom_check_stock/custom_check_stock',
#             'objects': http.request.env['custom_check_stock.custom_check_stock'].search([]),
#         })

#     @http.route('/custom_check_stock/custom_check_stock/objects/<model("custom_check_stock.custom_check_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_check_stock.object', {
#             'object': obj
#         })
