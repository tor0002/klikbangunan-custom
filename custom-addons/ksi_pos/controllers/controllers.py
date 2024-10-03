# -*- coding: utf-8 -*-
# from odoo import http


# class KsiPos(http.Controller):
#     @http.route('/ksi_pos/ksi_pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_pos/ksi_pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_pos.listing', {
#             'root': '/ksi_pos/ksi_pos',
#             'objects': http.request.env['ksi_pos.ksi_pos'].search([]),
#         })

#     @http.route('/ksi_pos/ksi_pos/objects/<model("ksi_pos.ksi_pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_pos.object', {
#             'object': obj
#         })
