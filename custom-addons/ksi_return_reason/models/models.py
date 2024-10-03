# -*- coding: utf-8 -*-

from email.policy import default
from typing_extensions import Required
from odoo import models, fields, api


# class ksi_return_reason(models.Model):
#     _name = 'ksi_return_reason.ksi_return_reason'
#     _description = 'ksi_return_reason.ksi_return_reason'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class ReturnReason(models.Model):
    _name = 'return.reason'
    _description = 'Return Reason'
    
    name = fields.Char('Keterangan', required=True)

class Picking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking Inherit KSI'

    # custom_reason = fields.Text(string='Custom Reason', compute="_get_return_reason", store=True)
    status = fields.Boolean('Return', compute="_get_return_reason")
    return_line = fields.One2many('stock.return.picking', 'picking_id', string='Return')
    return_reason = fields.Char('Return Reason', readonly=True, compute='_get_return_reason')

    @api.depends('return_line')
    def _get_return_reason(self):
        line_reason = self.env['stock.return.picking'].search([('id','in',self.return_line.ids)])
        if line_reason and line_reason.reason_id:
            self.status = line_reason.status
            self.return_reason = line_reason.reason_id.name
        else :
            self.status = ""
            self.return_reason = ""

