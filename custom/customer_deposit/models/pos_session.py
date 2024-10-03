from odoo import api, fields, models, tools, _

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    def _validate_session(self):
        res = super(PosSession, self)._validate_session()
        self._set_update_deposit()
        return res

    def _set_update_deposit(self):
        partners = self.env['res.partner'].sudo().search([])
        for record in partners:
           record.update({'amount_deposit': record.deposit_amount})        

    def _create_account_move(self):
        res = super(PosSession, self)._create_account_move()
        for order in self.order_ids:
            if order.is_invoiced:
                order.account_move.mapped('line_ids').remove_move_reconcile()
        return res           