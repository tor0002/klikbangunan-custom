from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    is_deposit = fields.Boolean('Is Deposit')
                
    @api.onchange('is_deposit')
    def _onchange_is_deposit(self):
        for method in self:
            if method.is_deposit:
                method.split_transactions = True
            else:
                method.split_transactions = False