# -*- coding: utf-8 -*-
# from odoo import http


# class PriceRestricted2(http.Controller):
#     @http.route('/price_restricted_2/price_restricted_2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/price_restricted_2/price_restricted_2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('price_restricted_2.listing', {
#             'root': '/price_restricted_2/price_restricted_2',
#             'objects': http.request.env['price_restricted_2.price_restricted_2'].search([]),
#         })

#     @http.route('/price_restricted_2/price_restricted_2/objects/<model("price_restricted_2.price_restricted_2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('price_restricted_2.object', {
#             'object': obj
#         })
