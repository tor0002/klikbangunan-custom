from odoo import _, api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    def update_price_from_pricelist(self):
        for order in self.order_line:
            partner_name = self.partner_id.name
            pricelist = self.env['product.supplierinfo'].search([('name', '=', partner_name),('product_tmpl_id', '=', order.product_id.product_tmpl_id.id)])
            if pricelist:
                order.price_unit  = pricelist[0].price