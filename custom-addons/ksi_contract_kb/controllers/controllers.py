# -*- coding: utf-8 -*-
# from odoo import http


# class KsiEmployeeKb(http.Controller):
#     @http.route('/ksi_employee_kb/ksi_employee_kb', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_employee_kb/ksi_employee_kb/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_employee_kb.listing', {
#             'root': '/ksi_employee_kb/ksi_employee_kb',
#             'objects': http.request.env['ksi_employee_kb.ksi_employee_kb'].search([]),
#         })

#     @http.route('/ksi_employee_kb/ksi_employee_kb/objects/<model("ksi_employee_kb.ksi_employee_kb"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_employee_kb.object', {
#             'object': obj
#         })
