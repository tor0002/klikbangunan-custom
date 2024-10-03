# -*- coding: utf-8 -*-
# from odoo import http


# class CustomButton2(http.Controller):
#     @http.route('/custom_button_2/custom_button_2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_button_2/custom_button_2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_button_2.listing', {
#             'root': '/custom_button_2/custom_button_2',
#             'objects': http.request.env['custom_button_2.custom_button_2'].search([]),
#         })

#     @http.route('/custom_button_2/custom_button_2/objects/<model("custom_button_2.custom_button_2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_button_2.object', {
#             'object': obj
#         })
