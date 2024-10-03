from odoo import models, fields, api, _

class account_payment(models.Model):
    _inherit = "account.payment"
    
    def post(self):
        res = super(account_payment, self).post()
        active_model = self._context.get('active_model')
        if active_model == 'res.partner':
            partner = self.env['res.partner'].sudo().browse(self._context.get('active_id'))
            partner._set_update_deposit()
        return res