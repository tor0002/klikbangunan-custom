# -*- coding: utf-8 -*-
# from odoo import http


# class PosQty(http.Controller):
#     @http.route('/pos_qty/pos_qty', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_qty/pos_qty/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_qty.listing', {
#             'root': '/pos_qty/pos_qty',
#             'objects': http.request.env['pos_qty.pos_qty'].search([]),
#         })

#     @http.route('/pos_qty/pos_qty/objects/<model("pos_qty.pos_qty"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_qty.object', {
#             'object': obj
#         })
