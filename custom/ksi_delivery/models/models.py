# from odoo import models, fields

# class StockPickingBatch(models.Model):
#     _inherit = 'stock.picking.batch'

#     driver_id = fields.Many2one('drivers', string='Driver')
#     driver_name = fields.Char(related='driver_id.drivers_name', string='Driver Name', store=True)
#     driver_store = fields.Selection(related='driver_id.drivers_store', string='Driver Store', store=True)