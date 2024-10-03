from odoo import _, api, fields, models
from ast import literal_eval

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    def ksi_action_view_orderpoint(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_orderpoint")
        action['context'] = literal_eval(action.get('context'))
        action['context'].pop('search_default_trigger')
        action['context'].update({
                'search_default_product_id': self.product_id.id,
            })

        return action
        
