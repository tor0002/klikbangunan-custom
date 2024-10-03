# -*- coding: utf-8 -*-

# import json
# import time
# from ast import literal_eval
# from datetime import date, timedelta
# from itertools import groupby
# from operator import attrgetter, itemgetter
# from collections import defaultdict
# from turtle import pu

from odoo import SUPERUSER_ID, _, api, fields, models
# from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.exceptions import UserError
# from odoo.osv import expression
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_datetime
# from odoo.tools.float_utils import float_compare, float_is_zero, float_round
# from odoo.tools.misc import format_date

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Transfer (inherited by purchase_stock_picking_return_invoicing)'
    
    # def button_validate(self):
        # # Clean-up the context key at validation to avoid forcing the creation of immediate
        # # transfers.
        # ctx = dict(self.env.context)
        # ctx.pop('default_immediate_transfer', None)
        # self = self.with_context(ctx)

        # # Sanity checks.
        # pickings_without_moves = self.browse()
        # pickings_without_quantities = self.browse()
        # pickings_without_lots = self.browse()
        # products_without_lots = self.env['product.product']
        # for picking in self:
        #     if not picking.move_lines and not picking.move_line_ids:
        #         pickings_without_moves |= picking

        #     picking.message_subscribe([self.env.user.partner_id.id])
        #     picking_type = picking.picking_type_id
        #     precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        #     no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        #     no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in picking.move_line_ids)
        #     if no_reserved_quantities and no_quantities_done:
        #         pickings_without_quantities |= picking

        #     if picking_type.use_create_lots or picking_type.use_existing_lots:
        #         lines_to_check = picking.move_line_ids
        #         if not no_quantities_done:
        #             lines_to_check = lines_to_check.filtered(lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
        #         for line in lines_to_check:
        #             product = line.product_id
        #             if product and product.tracking != 'none':
        #                 if not line.lot_name and not line.lot_id:
        #                     pickings_without_lots |= picking
        #                     products_without_lots |= product

        # if not self._should_show_transfers():
        #     if pickings_without_moves:
        #         raise UserError(_('Please add some items to move.'))
        #     if pickings_without_quantities:
        #         raise UserError(self._get_without_quantities_error_message())
        #     if pickings_without_lots:
        #         raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(products_without_lots.mapped('display_name')))
        # else:
        #     message = ""
        #     if pickings_without_moves:
        #         message += _('Transfers %s: Please add some items to move.') % ', '.join(pickings_without_moves.mapped('name'))
        #     if pickings_without_quantities:
        #         message += _('\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(pickings_without_quantities.mapped('name'))
        #     if pickings_without_lots:
        #         message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (', '.join(pickings_without_lots.mapped('name')), ', '.join(products_without_lots.mapped('display_name')))
        #     if message:
        #         raise UserError(message.lstrip())

        # # Run the pre-validation wizards. Processing a pre-validation wizard should work on the
        # # moves and/or the context and never call `_action_done`.
        # if not self.env.context.get('button_validate_picking_ids'):
        #     self = self.with_context(button_validate_picking_ids=self.ids)
        # res = self._pre_action_done_hook()
        # if res is not True:
        #     return res

        # # Call `_action_done`.
        # if self.env.context.get('picking_ids_not_to_backorder'):
        #     pickings_not_to_backorder = self.browse(self.env.context['picking_ids_not_to_backorder'])
        #     pickings_to_backorder = self - pickings_not_to_backorder
        # else:
        #     pickings_not_to_backorder = self.env['stock.picking']
        #     pickings_to_backorder = self
        # pickings_not_to_backorder.with_context(cancel_backorder=True)._action_done()
        # pickings_to_backorder.with_context(cancel_backorder=False)._action_done()

        # if self.user_has_groups('stock.group_reception_report') \
        #         and self.user_has_groups('stock.group_auto_reception_report') \
        #         and self.filtered(lambda p: p.picking_type_id.code != 'outgoing'):
        #     lines = self.move_lines.filtered(lambda m: m.product_id.type == 'product' and m.state != 'cancel' and m.quantity_done and not m.move_dest_ids)
        #     if lines:
        #         # don't show reception report if all already assigned/nothing to assign
        #         wh_location_ids = self.env['stock.location']._search([('id', 'child_of', self.picking_type_id.warehouse_id.view_location_id.id), ('usage', '!=', 'supplier')])
        #         if self.env['stock.move'].search([
        #                 ('state', 'in', ['confirmed', 'partially_available', 'waiting', 'assigned']),
        #                 ('product_qty', '>', 0),
        #                 ('location_id', 'in', wh_location_ids),
        #                 ('move_orig_ids', '=', False),
        #                 ('picking_id', 'not in', self.ids),
        #                 ('product_id', 'in', lines.product_id.ids)], limit=1):
        #             action = self.action_view_reception_report()
        #             action['context'] = {'default_picking_ids': self.ids}
        #             return action
        # return True

        # res = super().button_validate()
        # picking_type = self.env['stock.picking.type'].search([('id', '=', self.picking_type_id.id)])
        # print("PICKING TYPE", picking_type.name, picking_type.name.lower())
        # if picking_type.name.lower() in 'returns':
        #     print("RETURN!")
        #     if self.from_purchase:
        #         print("FROM PURCHASE!", self.origin)
        #         group_id = self.env['procurement.group'].search([('id', '=', self.group_id.id)])
        #         purchase_id = self.env['purchase.order'].search([('name', '=', group_id.name)])
        #         print("PURCHASE: ", purchase_id.name)
        #         if purchase_id.invoice_count > 0:
        #             print("SUDAH ADA VENDOR BILL!")
        #             purchase_id.action_create_invoice_refund()
        # else:
        #     print("NORMAL!")
        # raise UserError("TEST button_validate !!!")
        # return res
        
    def _action_done(self):
        """Call `_action_done` on the `stock.move` of the `stock.picking` in `self`.
        This method makes sure every `stock.move.line` is linked to a `stock.move` by either
        linking them to an existing one or a newly created one.

        If the context key `cancel_backorder` is present, backorders won't be created.

        :return: True
        :rtype: bool
        """
        
        # print("SELF >>>>>>>>>>", self)
        # print("SELF ID >>>>>>>>>>", self.id)
        
        context = self._context or {}
        # print("CONTEXT >>>>>>>", context)
        
        # raise UserError("TEST _action_done ATAS !!!")
        
        res = super()._action_done()
        
        if 'button_validate_picking_ids' in context:
            if context['button_validate_picking_ids']:
                # print("button_validate_picking_ids", context['button_validate_picking_ids'][0])
                
                self_id = self.env['stock.picking'].search([('id', '=', context['button_validate_picking_ids'][0])])
                
                picking_type = self.env['stock.picking.type'].search([('id', '=', self_id.picking_type_id.id)])
                # print("PICKING TYPE", picking_type.name)
                if picking_type.name.lower() in 'returns':
                    print("RETURN!")
                    if self.purchase_id:
                        # print("SELF PURCHASE >>>>>>>", self.purchase_id)
                        if self.purchase_id.invoice_count > 0:
                            print("SUDAH ADA VENDOR BILL!")
                            # self.purchase_id.action_create_invoice_refund()
                            self.purchase_id.with_context(create_refund=True, default_move_type='in_refund').action_create_invoice_refund()    
                else:
                    print("NORMAL!")
                # raise UserError("TEST _action_done BAWAH !!!")
        
        return res