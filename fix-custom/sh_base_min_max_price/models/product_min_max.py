from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    pro_min_sale_price = fields.Float(string='Minimum Sale Price')
    pro_max_sale_price = fields.Float(string='Maximum Sale Price')
    
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    x_min_sale_price = fields.Float(string='Minimum Sale Price', related='product_variant_ids.pro_min_sale_price', readonly=False)
    x_max_sale_price = fields.Float(string='Maximum Sale Price', related='product_variant_ids.pro_max_sale_price', readonly=False)
    
