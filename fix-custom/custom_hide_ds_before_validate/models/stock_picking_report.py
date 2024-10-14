from odoo import models, _
from odoo.exceptions import ValidationError

class ReportDeliverySlip(models.AbstractModel):
    _name = 'report.stock.report_deliveryslip'
    _description = 'Delivery Slip Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        # Cek apakah semua dokumen dalam state 'done'
        for doc in docs:
            if doc.state != 'done':
                raise ValidationError(_('Cannot print delivery slip because the picking is not done.'))
        return {
            'docs': docs,
            'state': docs.mapped('state'),
        }
