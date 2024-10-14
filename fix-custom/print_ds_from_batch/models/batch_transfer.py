from odoo import models

class PickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    def action_print_delivery_slips(self):
        # Mendapatkan semua pickings yang ada di batch ini
        pickings = self.mapped('picking_ids')
        
        # Mencetak delivery slips untuk setiap pickings
        return self.env.ref('stock.action_report_delivery').report_action(pickings)
