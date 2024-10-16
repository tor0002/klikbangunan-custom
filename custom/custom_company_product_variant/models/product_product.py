from odoo import fields, api, models

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    x_company_id = fields.Many2one(
        'res.company', 'Company', index=1)