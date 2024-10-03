from odoo import _,api,models,fields

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    _description = 'Stock Move Line (inherited by ksi_adjustment_kb)'

