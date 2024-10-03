
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'
    _description = 'Backorder Confirmation (inherited by ksi_stock_kb'
    
    is_sale = fields.Boolean(compute='_compute_is_sale', string='Is Sale?')
    
    @api.depends('pick_ids')
    def _compute_is_sale(self):
        # pass
        for me in self:
            # print("SALE: CONTEXT >>>", me.env.context)
            # print("SALE: PICK IDS >>>", me.pick_ids)
            picking_line = me.pick_ids #me.pick_ids.search([], limit=1)
            # print("SALE: PICKING LINE >>>", picking_line)
            for line in picking_line:
                # print("SALE: LINE NAME >>>", line.name)
                picking_type = me.env['stock.picking.type'].search([('id', '=', line.picking_type_id.id)])
                print("SALE: PICKING TYPE >>>", picking_type.name, picking_type.code)
                if picking_type.code == 'outgoing': #Delivery Order from Sale Order
                    me.is_sale = True
                else:
                    me.is_sale = False
    
    is_purchase = fields.Boolean(compute='_compute_is_purchase', string='Is Purchase?')
    
    @api.depends('pick_ids')
    def _compute_is_purchase(self):
        # pass
        for me in self:
            # print("PURCHASE: CONTEXT >>>", me.env.context)
            # print("PURCHASE: PICK IDS >>>", me.pick_ids)
            picking_line = me.pick_ids #me.pick_ids.search([], limit=1)
            for line in picking_line:
                # print("PURCHASE: LINE NAME >>>", line.name)
                picking_type = me.env['stock.picking.type'].search([('id', '=', line.picking_type_id.id)])
                print("PURCHASE: PICKING TYPE >>>", picking_type.name, picking_type.code)
                if picking_type.code == 'incoming': #Receipt Order from Purchase Order
                    me.is_purchase = True
                else:
                    me.is_purchase = False

    def process(self):
        res = super(StockBackorderConfirmation, self).process()
        for rec in self.pick_ids:
            # print("dito >>>>>>>",rec.name)
            rec._create_inv_and_bill_from_warehouse(inv=True)
        return res