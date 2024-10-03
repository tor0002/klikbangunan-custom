from odoo import _,api,models,fields  

class StockMove(models.Model):
    _inherit = 'stock.move'
    _description = 'Stock Move'

    custom_customer_note = fields.Char('Customer Note', compute='_compute_custom_customer_note')
    custom_weight = fields.Float('Weight', compute='_compute_weight_from_product')
    total_weight = fields.Float('Total Weight', compute='_compute_custom_weight')

    @api.depends('picking_id.origin')
    def _compute_custom_customer_note(self):
        # self.custom_customer_note = self.picking_id.name
        for move in self:
            move.custom_customer_note = '' #perlu diperhatikan lesson dr lord aul
            print('dito test>>>>>>>>>>>>>>',move.picking_id.name)
            if move.picking_id and move.picking_id.origin:
                pos_order = self.env['pos.order'].search([('name', '=', move.picking_id.origin)], limit=1)
                if pos_order:
                    # pos_order_line = pos_order.lines.filtered(
                    #     lambda line: line.product_id == move.product_id
                    # ).limit(1)
                    # if pos_order_line:
                    #     move.custom_customer_note = pos_order_line.customer_note
                    for line in pos_order.lines:  # Iterate through pos_order_line records
                        if line.product_id == move.product_id:
                            move.custom_customer_note = line.customer_note
                            # Optional: Early termination if you want only one match
                            # break  # Uncomment to stop after first matching note
    
    @api.depends('custom_weight','quantity_done')
    def _compute_custom_weight(self):
        for line in self:
            line.total_weight = line.custom_weight * line.quantity_done

    @api.depends('product_id')
    def _compute_weight_from_product(self):
        for line in self:
            line.custom_weight = line.product_id.weight