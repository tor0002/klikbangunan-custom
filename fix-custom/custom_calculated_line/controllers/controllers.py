# -*- coding: utf-8 -*-
# from odoo import http


# class CustomCalculatedLine(http.Controller):
#     @http.route('/custom_calculated_line/custom_calculated_line', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_calculated_line/custom_calculated_line/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_calculated_line.listing', {
#             'root': '/custom_calculated_line/custom_calculated_line',
#             'objects': http.request.env['custom_calculated_line.custom_calculated_line'].search([]),
#         })

#     @http.route('/custom_calculated_line/custom_calculated_line/objects/<model("custom_calculated_line.custom_calculated_line"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_calculated_line.object', {
#             'object': obj
#         })
