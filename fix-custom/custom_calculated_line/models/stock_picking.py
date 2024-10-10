from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    x_total_lines = fields.Float(string='Total Lines', compute='_compute_total_lines')
    
    @api.depends('move_lines')
    def _compute_total_lines(self):
        for picking in self:
            # Menghitung jumlah total lines dalam move_lines
            total_lines = len(picking.move_lines)
            picking.x_total_lines = total_lines
