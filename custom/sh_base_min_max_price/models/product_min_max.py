from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    pro_min_sale_price = fields.Float(string='Minimum Sale Price')
    pro_max_sale_price = fields.Float(string='Maximum Sale Price')
