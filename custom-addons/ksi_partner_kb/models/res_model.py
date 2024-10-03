from odoo import _,fields,models,api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # customer_sequence = fields.Char('Customer Sequence', readonly=False, related='company_id.customer_sequence')
    # supplier_sequence = fields.Char('Supplier Sequence', readonly=False, related='company_id.supplier_sequence')
    # member_sequence = fields.Char('Member Sequence', readonly=False, related='company_id.member_sequence')
    
    initial_account_payable_id = fields.Many2one('account.account', string='Initial Account Payable', readonly=False, related='company_id.initial_account_payable_id')
    initial_account_receivable_id = fields.Many2one('account.account', string='Initial Account Receivable', readonly=False, related='company_id.initial_account_receivable_id')
    
class ResCompany(models.Model):
    _inherit = 'res.company'    

    # customer_sequence = fields.Char('Customer Sequence')
    # supplier_sequence = fields.Char('Supplier Sequence')
    # member_sequence = fields.Char('Member Sequence')
    
    initial_account_payable_id = fields.Many2one('account.account', string='Initial Account Payable')
    initial_account_receivable_id = fields.Many2one('account.account', string='Initial Account Receivable')
    