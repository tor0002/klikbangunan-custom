from odoo import api, fields, models, tools, _

class PosOrder(models.Model):
    _inherit = "pos.order"
    
    @api.model
    def _process_order(self, order, draft, existing_order):
        res = super(PosOrder, self)._process_order(order, draft, existing_order)
        orders = self.env['pos.order'].browse(res)
        for order in orders:
            deposit = 0.0        
            if any(payment.payment_method_id.is_deposit for payment in order.payment_ids):
                deposit += sum(payment.amount for payment in order.payment_ids)
            current_deposit = order.partner_id.amount_deposit
            order.partner_id.update({
                'amount_deposit': current_deposit - deposit,
            })
        return res