# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPopupAttach(http.Controller):
#     @http.route('/custom_popup_attach/custom_popup_attach', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_popup_attach/custom_popup_attach/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_popup_attach.listing', {
#             'root': '/custom_popup_attach/custom_popup_attach',
#             'objects': http.request.env['custom_popup_attach.custom_popup_attach'].search([]),
#         })

#     @http.route('/custom_popup_attach/custom_popup_attach/objects/<model("custom_popup_attach.custom_popup_attach"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_popup_attach.object', {
#             'object': obj
#         })
