from odoo import models, api
from odoo.exceptions import UserError

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    def action_done(self):
        for batch in self:
            # Memeriksa apakah batch memiliki lampiran
            if not batch.message_main_attachment_id:
                raise UserError('LAKUKAN ATTACHMENT PADA SURAT JALAN SEBELUM VALIDATE BATCH!!!')
        
        # Jika batch memiliki lampiran, lanjutkan proses validasi batch
        return super(StockPickingBatch, self).action_done()
