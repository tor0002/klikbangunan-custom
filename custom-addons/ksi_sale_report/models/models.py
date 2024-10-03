from odoo import _, api, fields, models
from datetime import datetime
class KsiSaleReportWizard(models.TransientModel):
    _name = 'ksi.sale.report.wizard'
    _description = 'Ksi sale Report Wizard'

    def get_default_crm(self):
        return self.env['crm.team'].search([('name', '=', 'Sales')]).ids

    def get_default_month(self):
        datem = datetime.today().strftime("%m")
        return datem
        
    name = fields.Char('NAMA REPORT?')
    group_by = fields.Selection([
        ('month', 'Month'),
        ('week', 'Week'),
    ], string='Group By', default='month')
    date = fields.Date('date')
    company_ids = fields.Many2many('res.company', string='Company',default=lambda self: self.env.user.company_ids)
    month = fields.Selection([
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'), 
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ], string='Month', default=get_default_month)
    crm_ids = fields.Many2many('crm.team', string='Sales Team', default=get_default_crm )
    year = fields.Selection([(str(num), str(num)) for num in range(2020, (datetime.now().year)+1 )], 'Year', default=str(datetime.now().year))

    def generate_report(self):
        return self.env.ref('ksi_sale_report.ksi_report_custom_sale_action').report_action(self)  

    