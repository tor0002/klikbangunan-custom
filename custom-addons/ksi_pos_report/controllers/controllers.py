# -*- coding: utf-8 -*-
# from odoo import http


# class KsiPosReport(http.Controller):
#     @http.route('/ksi_pos_report/ksi_pos_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_pos_report/ksi_pos_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_pos_report.listing', {
#             'root': '/ksi_pos_report/ksi_pos_report',
#             'objects': http.request.env['ksi_pos_report.ksi_pos_report'].search([]),
#         })

#     @http.route('/ksi_pos_report/ksi_pos_report/objects/<model("ksi_pos_report.ksi_pos_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_pos_report.object', {
#             'object': obj
#         })
