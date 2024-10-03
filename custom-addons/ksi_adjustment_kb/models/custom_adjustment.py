from odoo import _,api,models,fields

class CustomAdjustment(models.Model):
    _name = 'custom.adjustment'
    _description = 'Custom Adjustment'
    
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )
    description = fields.Text(string='Keterangan')