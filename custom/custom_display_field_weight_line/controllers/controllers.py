# -*- coding: utf-8 -*-
# from odoo import http


# class CustomDisplayFieldWeightLine(http.Controller):
#     @http.route('/custom_display_field_weight_line/custom_display_field_weight_line', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_display_field_weight_line/custom_display_field_weight_line/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_display_field_weight_line.listing', {
#             'root': '/custom_display_field_weight_line/custom_display_field_weight_line',
#             'objects': http.request.env['custom_display_field_weight_line.custom_display_field_weight_line'].search([]),
#         })

#     @http.route('/custom_display_field_weight_line/custom_display_field_weight_line/objects/<model("custom_display_field_weight_line.custom_display_field_weight_line"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_display_field_weight_line.object', {
#             'object': obj
#         })
