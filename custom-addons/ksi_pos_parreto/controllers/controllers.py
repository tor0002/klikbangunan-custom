# -*- coding: utf-8 -*-
# from odoo import http


# class KsiPosParreto(http.Controller):
#     @http.route('/ksi_pos_parreto/ksi_pos_parreto', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_pos_parreto/ksi_pos_parreto/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_pos_parreto.listing', {
#             'root': '/ksi_pos_parreto/ksi_pos_parreto',
#             'objects': http.request.env['ksi_pos_parreto.ksi_pos_parreto'].search([]),
#         })

#     @http.route('/ksi_pos_parreto/ksi_pos_parreto/objects/<model("ksi_pos_parreto.ksi_pos_parreto"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_pos_parreto.object', {
#             'object': obj
#         })
