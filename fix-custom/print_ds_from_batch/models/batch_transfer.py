from odoo import models, api
from odoo.exceptions import UserError

class PickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    def action_print_delivery_slips(self):
        # Memastikan state batch adalah 'done'
        if self.state != 'done':
            raise UserError('Cannot print delivery slips because the batch is not done.')
        
        # Mendapatkan semua pickings yang ada di batch ini
        pickings = self.mapped('picking_ids')
        
        # Mencetak delivery slips untuk setiap pickings
        return self.env.ref('stock.action_report_delivery').report_action(pickings)
