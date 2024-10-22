# -*- coding: utf-8 -*-
# from odoo import http


# class CustomProductCategory(http.Controller):
#     @http.route('/custom_product_category/custom_product_category', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_product_category/custom_product_category/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_product_category.listing', {
#             'root': '/custom_product_category/custom_product_category',
#             'objects': http.request.env['custom_product_category.custom_product_category'].search([]),
#         })

#     @http.route('/custom_product_category/custom_product_category/objects/<model("custom_product_category.custom_product_category"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_product_category.object', {
#             'object': obj
#         })
