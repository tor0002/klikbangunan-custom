from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    x_min_price = fields.Float(string='Min Price', related='product_variant_ids.')
    