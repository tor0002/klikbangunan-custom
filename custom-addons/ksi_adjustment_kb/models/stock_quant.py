# import http
# from pyparsing import line
from odoo import _,api,models,fields
# from http import redirect
# import requests as req


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    _description = 'Stock Quantity (inherited by ksi_adjustment_kb)'

    def open_view(self):
        print(">>>>>>> TIMESTAMP", fields.datetime.now())
    
        # for rec in self:
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'view_mode': 'form',
        #         'res_model': 'sale.order', #rec._name,
        #         # 'view_id': self.env.ref('ksi_adjustment_kb.stock_view_move_line_tree_inherit_ksi_adjustment_kb_action').id,
        #         'target': 'current',
        #         'res_id': rec.id,
        #     }
        
        # action = self.env.ref('ksi_adjustment_kb.stock_view_move_line_tree_inherit_ksi_adjustment_kb_action')
        # return req.get('http://localhost:9045/web#menu_id=217&cids=1&action=%s' % (action.id))
        
        # context="{'id':id,'name_related':name_related}
        
        # return {
        #     'name': ('Inventory References'),
        #     'view_type': 'tree',
        #     'view_mode': 'tree',
        #     'res_model': 'stock.move.line',
        #     'view_id': self.env.ref('ksi_adjustment_kb.stock_view_move_line_tree_inherit_ksi_adjustment_kb_action').id,
        #     'type': 'ir.actions.act_window',
        #     'target':'new'
        # }

        pass
