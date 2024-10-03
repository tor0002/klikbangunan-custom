# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerDepositRealtime(http.Controller):
#     @http.route('/customer_deposit_realtime/customer_deposit_realtime', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_deposit_realtime/customer_deposit_realtime/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_deposit_realtime.listing', {
#             'root': '/customer_deposit_realtime/customer_deposit_realtime',
#             'objects': http.request.env['customer_deposit_realtime.customer_deposit_realtime'].search([]),
#         })

#     @http.route('/customer_deposit_realtime/customer_deposit_realtime/objects/<model("customer_deposit_realtime.customer_deposit_realtime"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_deposit_realtime.object', {
#             'object': obj
#         })
