from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    list_price = fields.Float(tracking=True)

