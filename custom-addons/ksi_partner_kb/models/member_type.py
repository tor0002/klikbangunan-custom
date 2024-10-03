from odoo import _, api, fields, models

class MemberType(models.Model):
    _name = 'member.type'
    _description = 'Member Type (new by ksi_partner_kb)'
    
    name = fields.Char('Name', required=True)