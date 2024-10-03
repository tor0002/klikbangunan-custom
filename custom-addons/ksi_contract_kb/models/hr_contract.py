from odoo import _, api, fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    tunjangan = fields.Monetary('Tunjangan')
    potongan = fields.Monetary('Potongan')

    tunjangan_jabatan = fields.Monetary('Tunjangan Jabatan')
    komunikasi = fields.Monetary('Komunikasi')
    pph21 = fields.Monetary('Pph21')
    bpjs_kes = fields.Monetary('Bpjs Kesehatan')

    gaji_harian = fields.Monetary(compute='_compute_gaji_harian', string='Gaji Harian', store=True, help='Dasar Perhitungan Bonus/Potongan')
    # tes_reja = fields.Char('tes_reja')


 


    @api.depends('structure_type_id','wage')
    def _compute_gaji_harian(self):
        for rec in self:
            if rec.wage > 0 and rec.structure_type_id.name == 'Weekly':
                # print('dito check >>>>>>>>>>>>', rec.structure_type_id.name)
                rec.gaji_harian = rec.wage / 26
            else:
                rec.gaji_harian = rec.wage / 25
 
   