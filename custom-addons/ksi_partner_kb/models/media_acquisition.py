from odoo import _, api, fields, models

class MediaAcquisition(models.Model):
    _name = 'media.acquisition'
    _description = 'Media Acquisition (new from ksi_partner_kb)'
    
    name = fields.Char('Name', required=True)
    