from odoo import models, api, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_price = fields.Float('Minimum Price')
    max_price = fields.Float('Maximum Price')