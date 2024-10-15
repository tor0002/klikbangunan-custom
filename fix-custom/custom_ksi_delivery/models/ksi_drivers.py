from odoo import fields, models

class KSIDrivers(models.Model):
    _name = 'ksi.drivers'
    _rec_name = 'x_drivers_name'
    
    x_drivers_name = fields.Char(string='Nama Driver', required=True)