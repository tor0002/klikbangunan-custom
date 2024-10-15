# -*- coding: utf-8 -*-
# from odoo import http


# class CustomKsiDelivery(http.Controller):
#     @http.route('/custom_ksi_delivery/custom_ksi_delivery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_ksi_delivery/custom_ksi_delivery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_ksi_delivery.listing', {
#             'root': '/custom_ksi_delivery/custom_ksi_delivery',
#             'objects': http.request.env['custom_ksi_delivery.custom_ksi_delivery'].search([]),
#         })

#     @http.route('/custom_ksi_delivery/custom_ksi_delivery/objects/<model("custom_ksi_delivery.custom_ksi_delivery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_ksi_delivery.object', {
#             'object': obj
#         })
