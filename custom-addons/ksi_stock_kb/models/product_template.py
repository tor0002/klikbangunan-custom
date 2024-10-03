from email.policy import default
from odoo import _, api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template (inherited by ksi_stock_kb)'
    
    nama_merk = fields.Char('Nama Merk', default='')
    keterangan = fields.Char('Keterangan', default='')
    kemasan = fields.Char('Kemasan', default='')
    ukuran = fields.Char('Ukuran', default='')
    auto_barcode = fields.Char(compute='_compute_auto_barcode', string='Auto Barcode', store=True)
    merk_prefix = fields.Char('Prefix Merk')
    barcode_and_seq = fields.Char('Barcode and seq', default="default barandseq")
    parrent_category = fields.Char('Parent Category',compute='_field_parent_category', store=True)
    
    @api.depends('categ_id')
    def _field_parent_category(self):
        for rec in self:
            if rec.categ_id:
                # tags_ids = [line.name for line in rec.category_id if line.name]
                # if tags_ids:
                rec.parrent_category = rec.categ_id.name
            if rec.categ_id.parent_id:
                rec.parrent_category = rec.categ_id.parent_id.name

    # ! Function dapatkan barcode_seq parentnya product_categ
    def _get_parent_barcode_sequence(self, product_categ):
        if product_categ.parent_id:
            barcode_seq_item = product_categ.parent_id.barcode_sequence
            if barcode_seq_item:
                return barcode_seq_item
            else:
                barcode_seq_item = "kosong"
                return barcode_seq_item

        # ! Kalo gk punya parent
        else:
            return False


    @api.depends('categ_id','merk_prefix')
    def _compute_auto_barcode(self):
        for rec in self:
            # ! Kalau barcodenya udah ada, gk usah di assign
            # !Recursive
            barcode_seq_list = [rec.categ_id.barcode_sequence or ""]
            product_categ = rec.categ_id
            isParent = True
            while isParent == True:
                get_barcode = self._get_parent_barcode_sequence(product_categ)
                if get_barcode:
                    if get_barcode != "kosong":
                        barcode_seq_list.append(get_barcode)
                    product_categ = product_categ.parent_id
                else:
                    isParent = False

            # ! Reverse list dari belakang
            def reverse_list(lst):
                lst.reverse()
                return lst
                
            if barcode_seq_list:
                barcode_list_reversed = reverse_list(barcode_seq_list)
                barcode_seq = ""
                hasil = barcode_seq.join(barcode_list_reversed)
                merk = ""
                if rec.merk_prefix:
                    merk = rec.merk_prefix.upper()
                rec.auto_barcode = merk + hasil

                # ! Masukin ke variable yang bukan compute karna gatau knp harus gini
                rec.barcode_and_seq = merk + hasil
            
            else:
                rec.auto_barcode = rec.categ_id.name_get()[0][1].split(' / ')
                rec.auto_barcode = ""        


    # ! Onchange name product depends on the field
    @api.onchange('nama_merk', 'keterangan', 'kemasan', 'ukuran')
    def _onchange_name(self):
        self.nama_merk = self.nama_merk.upper() if self.nama_merk else ""
        self.keterangan = self.keterangan.upper() if self.keterangan else ""
        self.kemasan = self.kemasan.upper() if self.kemasan else ""
        self.ukuran = self.ukuran.upper() if self.ukuran else ""
        
        nama_merk = self.nama_merk.strip()
        keterangan = self.keterangan.strip()
        kemasan = self.kemasan.strip()
        ukuran = self.ukuran.strip()
        
        new_name = " ".join([nama_merk, keterangan, kemasan, ukuran]) #nama_merk + keterangan + kemasan + ukuran
        self.name = new_name.strip()
        
        
    @api.model
    def create(self, vals):
        result = super().create(vals)
        # ! Untuk sequence
        if not result.barcode:
            tampung2 = self.env['ir.sequence'].next_by_code('ksi.unique.barcode')
            tampung = vals["barcode_and_seq"]
            if tampung and tampung2:
                # ! Kalo kode gk ada isinya pake or
                hasil = tampung + tampung2
                vals["barcode"] = hasil
                result.barcode = hasil
                result.default_code = hasil
                return result
            else:
                msg = _("Please insert Prefix merk or Product Category Barcode Sequence")
                raise UserError(msg)
        # ! Apabila barcode diisi manual
        else:
            return result

