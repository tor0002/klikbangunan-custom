# -*- coding: utf-8 -*-
# from odoo import http


# class CustomHideDsBeforeValidate(http.Controller):
#     @http.route('/custom_hide_ds_before_validate/custom_hide_ds_before_validate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_hide_ds_before_validate/custom_hide_ds_before_validate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_hide_ds_before_validate.listing', {
#             'root': '/custom_hide_ds_before_validate/custom_hide_ds_before_validate',
#             'objects': http.request.env['custom_hide_ds_before_validate.custom_hide_ds_before_validate'].search([]),
#         })

#     @http.route('/custom_hide_ds_before_validate/custom_hide_ds_before_validate/objects/<model("custom_hide_ds_before_validate.custom_hide_ds_before_validate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_hide_ds_before_validate.object', {
#             'object': obj
#         })
