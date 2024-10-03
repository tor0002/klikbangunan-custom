from odoo import _,api,models,fields
import logging
_logger = logging.getLogger(__name__)

class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    def custom_action_replenish(self, rec=False, purchase=False):
        _logger.info('test %s' %purchase)
        if purchase:
            product_list = self.env['purchase.order.line'].search([('order_id', '=', purchase.id), 
                                                                   ('product_id', '=', rec.product_id.id)], limit=1)
            if not product_list:
                vals = {
                    'product_id': rec.product_id.id,
                    'product_qty': rec.qty_to_order,
                    'product_uom': rec.product_id.uom_id.id,
                    'price_unit': rec.product_id.standard_price,
                    'order_id': purchase.id,
                }
                rec.env['purchase.order.line'].create(vals)
            else:
                product_list.write({'product_qty': product_list.product_qty + rec.qty_to_order})
        
            
    def action_replenish(self):
        calls = False
        for rec in self:
            if rec.product_id.seller_ids:
                search_po = rec.env['purchase.order'].search([('state','=','draft'), 
                                                              ('partner_id','=',rec.product_id.seller_ids[0].name.id)],limit=1)
                if search_po:
                    rec.custom_action_replenish(rec=rec, purchase=search_po)
                else:
                    calls = True
        
        if calls:
            return super(StockWarehouseOrderpoint,self).action_replenish()