from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, AccessError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner (inherited by ksi_partner_kb)'
    
    # 1. select user_id from hr_employee where user_id is not null
    # 2. select * from res_users where id in #1
    def _get_user_id(self):
        user_list = []
        query = """select id from res_users where id in (select user_id from hr_employee where user_id is not null)"""
        self.env.cr.execute(query)
        result = self._cr.dictfetchall()
        for res in result:
            user_list.append(res['id'])
        return user_list
    
    alamat_pengiriman = fields.Text(string='Alamat Pengiriman')
    nomor_ktp = fields.Char('Nomor KTP')
    agama = fields.Char('Agama')
    jenis_kelamin = fields.Selection([
        ('lk', 'Laki-laki'), ('pr', 'Perempuan')
    ], string='Jenis Kelamin')
    nomor_member = fields.Char('Nomor Member', related='ref')
    member_type_id = fields.Many2one('member.type', string='Jenis Member')
    # jumlah_poin = fields.Char('Jumlah Poin')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    person_id = fields.Many2one('res.users', string='The Sales Person',
      help='The internal user in charge of this contact.',
      domain=lambda self: [('id','in',self._get_user_id())])
    tanggal_join = fields.Date('Tanggal Join')
    outlet_id = fields.Many2one('res.company', string='Registration Outlet (OLD)', default=lambda self: self.env.company)
    regout_id = fields.Many2one('registration.outlet', string='Registration Outlet')
    media_acquisition_id = fields.Many2one('media.acquisition', string='Media Akuisisi')
    media_akuisisi = fields.Char('Media Akuisisi' ,related="media_acquisition_id.name")
    tags = fields.Char('Tags',compute='_field_tags', store=True)
    # tukang = fields.Char('Tukang')

    alamat_npwp = fields.Text('Alamat NPWP')
    pic_1 = fields.Char('PIC 1')
    kontak_pic_1 = fields.Char('Kontak PIC 1')
    pic_2 = fields.Char('PIC 2')
    kontak_pic_2 = fields.Char('Kontak PIC 2')
    nomor_rekening = fields.Char('Nomor Rekening')
    metode_pembayaran = fields.Char('Metode Pembayaran')
    tipe_vendor = fields.Char('Tipe Vendor')
    principle = fields.Char('Principle')
    
    ref = fields.Char(string='Reference', index=True, readonly=False, default=lambda self: _('New'))

    @api.depends('category_id.name')
    def _field_tags(self):
        for rec in self:
            rec.tags = ''
            if rec.category_id:
                # tags_ids = [line.name for line in rec.category_id if line.name]
                # if tags_ids:
                rec.tags =', '.join(rec.category_id.mapped('name'))
    
    @api.model
    def create(self, vals):
        company_list = self.env['res.company'].search([]).sorted('id')
        # print("COMPANY LIST!!! >>>>>", company_list)
        
        for comp in company_list:
            if not comp.initial_account_payable_id.id or not comp.initial_account_receivable_id.id:
                msg = _(('Please check! Whether "Default Account Payable" nor "Default Account Receivable" is not defined yet for the company "%s"!') % (comp.name))
                raise UserError(msg)
            
        res = super(ResPartner, self).create(vals)
        
        # print("self.customer_rank", res.customer_rank)
        # print("self.supplier_rank", res.supplier_rank)
        
        # sequences = self.env['ir.sequence'].search([('code','=','res.partner')])
        # for seq in sequences:
        #     print("SEQ ID >>> ", seq.id)
        #     print("SEQ NAME >>> ", seq.name)
        #     print("SEQ PREFIX >>> ", seq.prefix)
        
        if res.ref=='New' and (res.customer_rank > 0 or res.supplier_rank == 0):
            res.ref = self.env['ir.sequence'].next_by_code('res.partner')
        
        for comp in company_list:
            res.with_company(comp.id).property_account_payable_id = comp.initial_account_payable_id.id
            res.with_company(comp.id).property_account_receivable_id = comp.initial_account_receivable_id.id
       
        return res
    
    def _get_initial_account_payable_id(self):
        acc_pay_sel = self.env.company.initial_account_payable_id.id
        # if acc_pay_sel and self.customer_rank > 0: return acc_pay_sel
        # print("PAYABLE CONTEXT:", self._context.get('customer_rank'))
        if acc_pay_sel: return acc_pay_sel 
    def _get_initial_account_receivable_id(self):
        acc_rec_sel = self.env.company.initial_account_receivable_id.id
        # if acc_rec_sel and self.customer_rank > 0: return acc_rec_sel
        # print("RECEIVABLE CONTEXT:", self._context.get('customer_rank'))
        if acc_rec_sel: return acc_rec_sel
            
    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
        string="Account Payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the payable account for the current partner",
        required=True, default=_get_initial_account_payable_id)
    property_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
        string="Account Receivable",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the receivable account for the current partner",
        required=True, default=_get_initial_account_receivable_id)