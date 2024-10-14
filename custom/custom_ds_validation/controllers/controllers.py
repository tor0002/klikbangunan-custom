# -*- coding: utf-8 -*-
# from odoo import http


# class CustomDsValidation(http.Controller):
#     @http.route('/custom_ds_validation/custom_ds_validation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_ds_validation/custom_ds_validation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_ds_validation.listing', {
#             'root': '/custom_ds_validation/custom_ds_validation',
#             'objects': http.request.env['custom_ds_validation.custom_ds_validation'].search([]),
#         })

#     @http.route('/custom_ds_validation/custom_ds_validation/objects/<model("custom_ds_validation.custom_ds_validation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_ds_validation.object', {
#             'object': obj
#         })
