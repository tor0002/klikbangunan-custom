from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order (inherited by ksi_sale_kb)'
    
    active = fields.Boolean(string='Active', default=True)
    invoice_refund_count = fields.Integer(
        compute="_compute_invoice_refund_count", string="# of Invoice Refunds"
    )
    
    # def action_confirm(self):
    #     res = super(SaleOrder, self).action_confirm()
    #     for picking in self.picking_ids:
    #         for move in picking.move_ids_without_package:
    #             move.custom_weight = move.sale_line_id.custom_weight
    #             move.total_weight = move.sale_line_id.total_weight
    #     return res
    
    def action_view_invoice_refund(self):
        self.sudo()._read(["invoice_ids"])
        invoices = self.invoice_ids
        refunds = invoices.filtered(lambda x: x.move_type == "out_refund")
        move_vals = []
        for picking in self.picking_ids:
            account_move = self.env['account.move'].sudo().search([('move_type', '=', 'out_refund'), ('ref', 'ilike', picking.name)], limit=1)
            if account_move:
                move_vals.append(account_move.id)
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_out_refund_type"
        )
        result["domain"] = [("id", "in", move_vals)]
        return result

    @api.depends("order_line.invoice_lines.move_id.state")
    def _compute_invoice_refund_count(self):
        for order in self:
            move_vals = []
            for picking in order.picking_ids:
                account_move = self.env['account.move'].sudo().search([('move_type', '=', 'out_refund'), ('ref', 'ilike', picking.name)], limit=1)
                if account_move:
                    move_vals.append(account_move.id)
            invoices = order.mapped("order_line.invoice_lines.move_id").filtered(
                lambda x: x.move_type == "out_refund"
            )
            order.invoice_refund_count = len(move_vals)
            

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sale Order Line (inherited by ksi_sale_kb)'

    product_cost = fields.Float('Product Cost', related='product_template_id.standard_price', store=True)
    # on_hand_qty = fields.Float('On-Hand Qty', related='product_template_id.qty_available', store=True)
    custom_weight = fields.Float('Weight', related='product_template_id.weight')
    total_weight = fields.Float('Total Weight',compute='_compute_custom_weight')

    @api.depends('custom_weight','product_uom_qty')
    def _compute_custom_weight(self):
        for line in self:
            line.total_weight = line.custom_weight * line.product_uom_qty