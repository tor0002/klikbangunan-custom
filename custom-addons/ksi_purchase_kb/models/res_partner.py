from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner (inherited by ksi_purchase_kb)'
    
    alamat_npwp = fields.Text('Alamat NPWP')
    pic_1 = fields.Char('PIC 1')
    kontak_pic_1 = fields.Char('Kontak PIC 1')
    pic_2 = fields.Char('PIC 2')
    kontak_pic_2 = fields.Char('Kontak PIC 2')
    nomor_rekening = fields.Char('Nomor Rekening')
    metode_pembayaran = fields.Char('Metode Pembayaran')
    tipe_vendor = fields.Char('Tipe Vendor')
    principle = fields.Char('Principle')