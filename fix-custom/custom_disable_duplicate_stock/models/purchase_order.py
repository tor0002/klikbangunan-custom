from odoo import fields, api, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    x_auto_purchase_order_id_sale_order_count = fields.Integer(
        string='Source Purchase Order count', compute='_compute_x_auto_purchase_order_id_sale_order_count')
    
    def _compute_x_auto_purchase_order_id_sale_order_count(self):
        for record in self:
            record['x_auto_purchase_order_id_sale_order_count'] = self.env['sale.order'].search_count(
                [('auto_purchase_order_id', '=', record.id)])
