# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPrintDs(http.Controller):
#     @http.route('/custom_print_ds/custom_print_ds', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_print_ds/custom_print_ds/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_print_ds.listing', {
#             'root': '/custom_print_ds/custom_print_ds',
#             'objects': http.request.env['custom_print_ds.custom_print_ds'].search([]),
#         })

#     @http.route('/custom_print_ds/custom_print_ds/objects/<model("custom_print_ds.custom_print_ds"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_print_ds.object', {
#             'object': obj
#         })
