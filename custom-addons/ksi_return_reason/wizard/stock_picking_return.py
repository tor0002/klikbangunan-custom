# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from email.policy import default
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round

class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'
    _description = 'Return Picking Inherit KSI'

    # select code from stock_picking_type group by code
    # 
    # 	code
    # 1	internal
    # 2	outgoing
    # 3	incoming
    # 4	mrp_operation

    picking_code = fields.Char(compute='_compute_picking_code', string='Picking Type Code')

    @api.depends('picking_id')
    def _compute_picking_code(self):
        # pass
        for me in self:
            operation_type = me.env['stock.picking.type'].search([('id','=',me.picking_id.picking_type_id.id)]).mapped('code')
            # if operation_type:
                # print("IS FROM PURCHASE? ", operation_type) 
            me.picking_code = str(operation_type[0]).lower()
        
    # return_reason = fields.Selection([
    #     ('1', 'Barang Kurang'),
    #     ('2', 'Barang Rusak'),
    #     ('3', 'Salah Administrasi'),
    #     ('4', 'Barang Tidak Ada'),
    #     ('5', 'Lain-Lain (isi di bawah):')
    # ], string='Return Reason', store=True)
    
    reason_id = fields.Many2one('return.reason', string='Return Reason', store=True)
    # custom_reason = fields.Text(string='Custom Reason', store=True)
    status = fields.Boolean('Return', store=True)
