from odoo import _, api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    nilai_disc = fields.Char('DISC')
    nilai_iq = fields.Char('IQ')
    nilai_papikostik = fields.Char('Papikostik')