from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        for line in move.line_ids:
            if line.account_id.user_type_id.type == 'receivable' and line.partner_id:
                deposit_balance = line.partner_id.deposit_balance - line.debit + line.credit
                line.partner_id.write({'deposit_balance': deposit_balance})
        return move
