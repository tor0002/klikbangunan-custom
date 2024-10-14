# -*- coding: utf-8 -*-
# from odoo import http


# class CustomWarningBatch(http.Controller):
#     @http.route('/custom_warning_batch/custom_warning_batch', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_warning_batch/custom_warning_batch/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_warning_batch.listing', {
#             'root': '/custom_warning_batch/custom_warning_batch',
#             'objects': http.request.env['custom_warning_batch.custom_warning_batch'].search([]),
#         })

#     @http.route('/custom_warning_batch/custom_warning_batch/objects/<model("custom_warning_batch.custom_warning_batch"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_warning_batch.object', {
#             'object': obj
#         })
