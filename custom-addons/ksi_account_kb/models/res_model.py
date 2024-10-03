from odoo import _,fields,models,api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sales_coa_discount_id = fields.Many2one('account.account', string='Sales Chart of Accounts', readonly=False,related='company_id.sales_coa_discount_id')
    purchases_coa_discount_id = fields.Many2one('account.account', string='Purchases Chart of Accounts', readonly=False,related='company_id.purchases_coa_discount_id')


class ResCompany(models.Model):
    _inherit = 'res.company'    

    sales_coa_discount_id = fields.Many2one('account.account', string='COA Sales')
    purchases_coa_discount_id = fields.Many2one('account.account', string='COA Purchases')