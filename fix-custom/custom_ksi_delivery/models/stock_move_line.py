from odoo import fields, models, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    x_custom_weight = fields.Float('Weight', compute='_compute_weight_from_product')
    x_total_weight = fields.Float('Total Weight', compute='_compute_custom_weight')
    
    x_custom_insentif = fields.Float('Insentif', compute='_compute_insentif_from_product')
    x_total_insentif = fields.Float('Total Insentif', compute='_compute_total_insentif')
    
    @api.depends('product_id')
    def _compute_weight_from_product(self):
        for line in self:
            line.x_custom_weight = line.product_id.weight
    
    @api.depends('x_custom_weight','qty_done')
    def _compute_custom_weight(self):
        for line in self:
            line.x_total_weight = line.x_custom_weight * line.qty_done
            
    @api.depends('product_id')
    def _compute_insentif_from_product(self):
        for line in self:
            line.x_custom_insentif = line.product_id.product_tmpl_id.product_insentif
            
    @api.depends('x_custom_insentif', 'qty_done','x_custom_weight')
    def _compute_total_insentif(self):
        for line in self:
            line.x_total_insentif = line.x_custom_insentif * line.qty_done * line.x_custom_weight