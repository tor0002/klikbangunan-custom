from odoo import models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _create_account_move(self, move=None):
        res = super(PosOrder, self)._create_account_move(move)
        for order in self:
            if order.partner_id:
                # Calculate the new deposit balance
                deposit_balance = order.partner_id.deposit_balance - order.amount_total
                order.partner_id.write({'deposit_balance': deposit_balance})
        return res
