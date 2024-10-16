# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPickingOperationView(http.Controller):
#     @http.route('/custom_picking_operation_view/custom_picking_operation_view', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_picking_operation_view/custom_picking_operation_view/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_picking_operation_view.listing', {
#             'root': '/custom_picking_operation_view/custom_picking_operation_view',
#             'objects': http.request.env['custom_picking_operation_view.custom_picking_operation_view'].search([]),
#         })

#     @http.route('/custom_picking_operation_view/custom_picking_operation_view/objects/<model("custom_picking_operation_view.custom_picking_operation_view"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_picking_operation_view.object', {
#             'object': obj
#         })
