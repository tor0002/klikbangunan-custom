# -*- coding: utf-8 -*-
# from odoo import http


# class KsiPricelist(http.Controller):
#     @http.route('/ksi_pricelist/ksi_pricelist', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_pricelist/ksi_pricelist/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_pricelist.listing', {
#             'root': '/ksi_pricelist/ksi_pricelist',
#             'objects': http.request.env['ksi_pricelist.ksi_pricelist'].search([]),
#         })

#     @http.route('/ksi_pricelist/ksi_pricelist/objects/<model("ksi_pricelist.ksi_pricelist"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_pricelist.object', {
#             'object': obj
#         })
