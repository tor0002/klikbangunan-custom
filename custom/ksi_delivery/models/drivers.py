from odoo import models, fields, api

class Drivers(models.Model):
    _name = 'drivers'
    
    drivers_name = fields.Char(string='Nama Driver', required=True)  
    drivers_store = fields.Selection([
        ('KB01', 'KB01'),
         ('KB02', 'KB02'),
          ('KB03', 'KB03'),
           ('KB05', 'KB05'),
            ('KB06', 'KB06'),  
            ('KB07', 'KB07'), 
    ], string='Toko', required=True)
    
    