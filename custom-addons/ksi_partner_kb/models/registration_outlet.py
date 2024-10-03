from odoo import _, api, fields, models

class RegistrationOutlet(models.Model):
    _name = 'registration.outlet'
    _description = 'Registration Outlet (new by ksi_partner_kb)'
    
    name = fields.Char('Name', required=True)