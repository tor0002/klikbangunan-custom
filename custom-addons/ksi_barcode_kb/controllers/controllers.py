# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception as _serialize_exception
from odoo.addons.web.controllers.main import Home
from odoo.addons.stock_barcode.controllers.stock_barcode import StockBarcodeController


# class KsiBarcodeKb(http.Controller):
#     @http.route('/ksi_barcode_kb/ksi_barcode_kb', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ksi_barcode_kb/ksi_barcode_kb/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ksi_barcode_kb.listing', {
#             'root': '/ksi_barcode_kb/ksi_barcode_kb',
#             'objects': http.request.env['ksi_barcode_kb.ksi_barcode_kb'].search([]),
#         })

#     @http.route('/ksi_barcode_kb/ksi_barcode_kb/objects/<model("ksi_barcode_kb.ksi_barcode_kb"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ksi_barcode_kb.object', {
#             'object': obj
#         })
class KSIStockBarcode(StockBarcodeController):
     def _try_open_product_location(self, barcode):
        """ If barcode represent a product, open a list/kanban view to show all
        the locations of this product.
        """
        result = request.env['product.product'].search_read([
            ('barcode', '=', barcode),
        ], ['id', 'display_name','barcode_ids'], limit=1)

        # ! Cari additional barcode
        if not result:
            result = request.env['product.product'].search_read([
                ('barcode_ids', '=', barcode),
            ], ['id', 'display_name','barcode_ids'], limit=1)

        # result2 = request.env['product.product'].search_read([
        #     ('barcode_ids', '=', barcode),
        # ], ['id', 'display_name'], limit=1)
        
        # print('==============================================');
        # print('==================== reza ====================');
        # print('==================== reja disini stockbarcodecontroller  ------------------>',result);
        # print('==================== reza ====================');
        # print('==============================================');
        # print('==============================================');
        # print('==================== reza ====================');
        # print('==================== result2    ------------------>',result2);
        # print('==================== reza ====================');
        # print('==============================================');
        
        
        if result:
            tree_view_id = request.env.ref('stock.view_stock_quant_tree').id
            kanban_view_id = request.env.ref('stock_barcode.stock_quant_barcode_kanban_2').id
            return {
                'action': {
                    'name': result[0]['display_name'],
                    'res_model': 'stock.quant',
                    'views': [(tree_view_id, 'list'), (kanban_view_id, 'kanban')],
                    'type': 'ir.actions.act_window',
                    'domain': [('product_id', '=', result[0]['id'])],
                    'context': {
                        'search_default_internal_loc': True,
                    },
                }
            }


# ! Nonaktif superuser / odoobot
class KSIHome(Home):
    @http.route('/web/become', type='http', auth='user', sitemap=False)
    def switch_to_admin(self):
        uid = request.env.user.id
        # if request.env.user._is_system():
        #     uid = request.session.uid = odoo.SUPERUSER_ID
        #     # invalidate session token cache as we've changed the uid
        #     request.env['res.users'].clear_caches()
        #     request.session.session_token = security.compute_session_token(request.session, request.env)
        
        return request.redirect(self._login_redirect(uid))