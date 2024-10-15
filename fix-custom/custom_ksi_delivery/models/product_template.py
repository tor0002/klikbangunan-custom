from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit='product.template'
    
    product_insentif = fields.Float(string='Nominal Insentif')
    