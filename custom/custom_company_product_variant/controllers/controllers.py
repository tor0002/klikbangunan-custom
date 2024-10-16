# -*- coding: utf-8 -*-
# from odoo import http


# class CustomCompanyProductVariant(http.Controller):
#     @http.route('/custom_company_product_variant/custom_company_product_variant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_company_product_variant/custom_company_product_variant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_company_product_variant.listing', {
#             'root': '/custom_company_product_variant/custom_company_product_variant',
#             'objects': http.request.env['custom_company_product_variant.custom_company_product_variant'].search([]),
#         })

#     @http.route('/custom_company_product_variant/custom_company_product_variant/objects/<model("custom_company_product_variant.custom_company_product_variant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_company_product_variant.object', {
#             'object': obj
#         })
