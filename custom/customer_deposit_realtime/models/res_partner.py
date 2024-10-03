from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_balance = fields.Float('total_balance', compute="compute_total_balance")
    deposit_ids = fields.One2many('deposit.partner', 'partner_id', string='Deposit')
    
    @api.depends('total_balance', 'deposit_ids')
    def _compute_total_balance(self):
        for record in self:
            record.total_balance = sum(line.balance for line in record.deposit_ids)

    # Buat list view dari model ini
    
    
    

