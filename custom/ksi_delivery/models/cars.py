from odoo import models, fields, api

class Cars(models.Model):
    _name = 'cars'
    
    cars = fields.Selection([
        ('CARRY', 'CARRY'),
        ('ENGKEL', 'ENGKEL'),
        ('TRUK', 'TRUK'),
    ], string='Mobil', required=True)
    
    