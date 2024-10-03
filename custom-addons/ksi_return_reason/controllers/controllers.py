# -*- coding: utf-8 -*-
# from odoo import http


# class KsiReturnReason(http.Controller):
#     @http.route('/ksi_return_reason/ksi_return_reason', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_return_reason/ksi_return_reason/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_return_reason.listing', {
#             'root': '/ksi_return_reason/ksi_return_reason',
#             'objects': http.request.env['ksi_return_reason.ksi_return_reason'].search([]),
#         })

#     @http.route('/ksi_return_reason/ksi_return_reason/objects/<model("ksi_return_reason.ksi_return_reason"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_return_reason.object', {
#             'object': obj
#         })
