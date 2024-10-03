# -*- coding: utf-8 -*-
# from odoo import http


# class KsiSaleReport(http.Controller):
#     @http.route('/ksi_sale_report/ksi_sale_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_sale_report/ksi_sale_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_sale_report.listing', {
#             'root': '/ksi_sale_report/ksi_sale_report',
#             'objects': http.request.env['ksi_sale_report.ksi_sale_report'].search([]),
#         })

#     @http.route('/ksi_sale_report/ksi_sale_report/objects/<model("ksi_sale_report.ksi_sale_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_sale_report.object', {
#             'object': obj
#         })
