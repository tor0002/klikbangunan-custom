from odoo import models, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            # Memeriksa apakah jenis picking adalah 'Receipt' (incoming shipments)
            if picking.picking_type_id.code == 'incoming':
                # Mengecek apakah ada lampiran pada transfer receipt
                if not picking.message_main_attachment_id:
                    raise UserError('LAKUKAN ATTACHMENT SURAT JALAN SEBELUM VALIDASI')
        # Jika ada lampiran atau jenis transfer bukan Receipt, lanjutkan proses validasi
        return super(StockPicking, self).button_validate()
