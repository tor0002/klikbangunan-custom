# -*- coding: utf-8 -*-
# from odoo import http


# class CustomMinmaxPrice(http.Controller):
#     @http.route('/custom_minmax_price/custom_minmax_price', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_minmax_price/custom_minmax_price/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_minmax_price.listing', {
#             'root': '/custom_minmax_price/custom_minmax_price',
#             'objects': http.request.env['custom_minmax_price.custom_minmax_price'].search([]),
#         })

#     @http.route('/custom_minmax_price/custom_minmax_price/objects/<model("custom_minmax_price.custom_minmax_price"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_minmax_price.object', {
#             'object': obj
#         })
