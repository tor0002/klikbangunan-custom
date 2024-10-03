from email.policy import default
from odoo import _, api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class KSIProductCategory(models.Model):
    _inherit = 'product.category'
    _description = 'Product Category'

    barcode_sequence = fields.Char('Barcode Sequence')    