# -*- coding: utf-8 -*-
# from odoo import http


# class KsiDelivery(http.Controller):
#     @http.route('/ksi_delivery/ksi_delivery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_delivery/ksi_delivery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_delivery.listing', {
#             'root': '/ksi_delivery/ksi_delivery',
#             'objects': http.request.env['ksi_delivery.ksi_delivery'].search([]),
#         })

#     @http.route('/ksi_delivery/ksi_delivery/objects/<model("ksi_delivery.ksi_delivery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_delivery.object', {
#             'object': obj
#         })
