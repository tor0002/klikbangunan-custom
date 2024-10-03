from odoo import models, fields, api
from datetime import datetime, timedelta, date


class RefusedOrder(models.TransientModel):
    _name = 'refused.order'
    _description = 'Refused Order'

    def _default_order(self):
        return self.env['purchase.order'].browse(self._context.get('active_id'))

    order_id = fields.Many2one('purchase.order', string='Purchase Order', readonly=True, default=_default_order)
    refused_reason = fields.Text(string='Refused Reason', required=True)

    def refused_order(self):
        self.order_id.refused_reason = self.refused_reason
        self.order_id.refused_date = datetime.now()
        self.order_id.refused_id = self.env.user.id
        self.order_id.is_refused = True
        self.order_id.state = 'cancel'
