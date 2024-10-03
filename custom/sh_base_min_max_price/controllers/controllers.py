# -*- coding: utf-8 -*-
# from odoo import http


# class ShBaseMinMaxPrice(http.Controller):
#     @http.route('/sh_base_min_max_price/sh_base_min_max_price', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sh_base_min_max_price/sh_base_min_max_price/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sh_base_min_max_price.listing', {
#             'root': '/sh_base_min_max_price/sh_base_min_max_price',
#             'objects': http.request.env['sh_base_min_max_price.sh_base_min_max_price'].search([]),
#         })

#     @http.route('/sh_base_min_max_price/sh_base_min_max_price/objects/<model("sh_base_min_max_price.sh_base_min_max_price"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sh_base_min_max_price.object', {
#             'object': obj
#         })
