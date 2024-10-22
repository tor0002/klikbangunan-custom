from odoo import fields, api, models

class CheckStock(models.Model):
    _name = 'check.stock'
    _description = 'Check Stock'

    # Field related ke model stock.warehouse.orderpoint
    orderpoint_id = fields.Many2one('stock.warehouse.orderpoint', string='Replenishment')
    
    x_product_id = fields.Many2one(related='orderpoint_id.product_id', string='Product', readonly=True)
    x_warehouse_id = fields.Many2one(related='orderpoint_id.warehouse_id', string='Warehouse', readonly=True)
    x_product_min_qty = fields.Float(related='orderpoint_id.product_min_qty', string='Minimum Quantity', readonly=True)
    x_product_max_qty = fields.Float(related='orderpoint_id.product_max_qty', string='Maximum Quantity', readonly=True)
    