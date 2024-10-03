from odoo import models, api, fields

class DepositPartner(models.Model):
    _name = 'deposit.partner'
    
    debit = fields.Float()
    credit = fields.Float()
    balance = fields.Float(compute="compute_balance")
    partner_id = fields.Many2one('res.partner', string='partner')
    
    @api.depends('debit,credit,balance')
    def _compute_balance(self):
        for record in self:
            record.balance = record.debit - record.credit
    
    
    