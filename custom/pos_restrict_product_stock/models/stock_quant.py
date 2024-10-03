# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging

_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
    _inherit = "stock.quant"
        
    def _notify_pos(self):
        notifications = []
        for quant in self:
            session_obj = self.env['pos.session'].search(
                [('state', '=', 'opened')])
            for each_session_user in session_obj.user_id:
                notifications.append(                        
                    [(self._cr.dbname, 'stock.pos', each_session_user.id), "stock_notification", {}])                    
        self.env['bus.bus']._sendmany(notifications)

    def write(self, vals):
        res = super().write(vals)
        self._notify_pos()
        return res    