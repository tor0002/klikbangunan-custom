from odoo import fields, models, api
from odoo.exceptions import UserError

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'
    
    x_drivers_name = fields.Many2one('ksi.drivers', string='Nama Driver', required=True)
    x_cars = fields.Selection([
        ('Carry', 'CARRY'),
        ('Engkel','ENGKEL'),
        ('Traga', 'TRAGA'),
        ('Motor','MOTOR'),
    ], string='Kendaraan', required=True)
    
    x_sum_total_insentif = fields.Float(string="Total Insentif", compute="_compute_sum_total_insentif", store=True)
    x_sum_total_weight = fields.Float(string="Total Weight", compute="_compute_sum_total_weight", store=True)
    x_sum_total_weight_insentif = fields.Float(string="Total Pendapatan Insentif", compute="_compute_total_insentif_drivers", store=True)
    
    @api.depends('picking_ids.move_line_ids.x_total_insentif')
    def _compute_sum_total_insentif(self):
        for batch in self:
            # Mendapatkan semua stock.move.line terkait dari picking_ids
            total = sum(batch.picking_ids.mapped('move_line_ids').mapped('x_total_insentif'))
            batch.x_sum_total_insentif = total
            
    @api.depends('picking_ids.move_line_ids.x_total_weight')
    def _compute_sum_total_weight(self):
        for batch in self:
            # Mendapatkan semua stock.move.line terkait dari picking_ids
            total = sum(batch.picking_ids.mapped('move_line_ids').mapped('x_total_weight'))
            batch.x_sum_total_weight = total
            
    @api.depends('x_sum_total_weight', 'x_sum_total_insentif')
    def _compute_total_insentif_drivers(self):
        for batch in self:
            batch.x_sum_total_weight_insentif = batch.x_sum_total_weight * batch.x_sum_total_insentif
            
    @api.constrains('x_sum_total_weight', 'x_cars')
    def _check_weight_limit(self):
        for batch in self:
            if batch.x_cars == 'Carry' and batch.x_sum_total_weight > 500:
                raise UserError('Berat total tidak boleh melebihi 500 untuk Carry')
            elif batch.x_cars == 'Engkel' and batch.x_sum_total_weight > 1000:
                raise UserError('Berat total tidak boleh melebihi 1000 untuk Engkel')
            
