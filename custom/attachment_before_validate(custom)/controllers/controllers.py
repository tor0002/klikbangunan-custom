# -*- coding: utf-8 -*-
# from odoo import http


# class AttachmentBeforeValidate(http.Controller):
#     @http.route('/attachment_before_validate/attachment_before_validate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/attachment_before_validate/attachment_before_validate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('attachment_before_validate.listing', {
#             'root': '/attachment_before_validate/attachment_before_validate',
#             'objects': http.request.env['attachment_before_validate.attachment_before_validate'].search([]),
#         })

#     @http.route('/attachment_before_validate/attachment_before_validate/objects/<model("attachment_before_validate.attachment_before_validate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('attachment_before_validate.object', {
#             'object': obj
#         })
