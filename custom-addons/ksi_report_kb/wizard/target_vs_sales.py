from odoo import _, api, fields, models
from datetime import datetime, time
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell


class TargetVsSalesWizard(models.TransientModel):
    _name = 'target.vs.sales.wizard'
    _description = 'Target Vs Sales Wizard'
    
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    company_ids = fields.Many2many('res.company', string='Company')

    def action_print(self):

        # ! ini salah
        # return self.env.ref('report_kb_target_vs_sales').report_action(self)  

        # ! self.env.ref "wajib_nama_modul?.report_kb_target_vs_sales"
        return self.env.ref('ksi_report_kb.report_kb_target_vs_sales').report_action(self)


# ! Model untuk file excel only
class ReportTargetVsSales(models.AbstractModel):
    _name = 'report.ksi_report_kb.target.vs.sales'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        print('==============================================');
        print('==================== reza ====================');
        print('==================== data    ------------------>', data);
        print('==================== reza ====================');
        print('==============================================');
        print('==============================================');
        print('==================== reza ====================');
        print('==================== obj    ------------------>', obj);
        print('==================== reza ====================');
        print('==============================================');
        for item in obj.company_ids:
            print('==============================================');
            print('==================== reza ====================');
            print('==================== item    ------------------>', item.name);
            print('==================== reza ====================');
            print('==============================================');
        
        # ! KOLOM A = 0
        # ! BARIS 1 = 0

        sheet = workbook.add_worksheet('KB Target Vs Sales')
        text_top_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'white', 'bg_color': '#b904bf', 'valign': 'vcenter'})
        text_header_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'white', 'bg_color': '#b904bf', 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        text_style = workbook.add_format({'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        number_style = workbook.add_format({'num_format': '#,##0', 'font_size': 12, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True})
 
        sheet.merge_range(0, 0, 0, 4, "Reference", text_top_style)
        sheet.write(1, 1, "sales harian & mtd klikbangunan", text_top_style)
        # sheet.merge_range(1, 0, 1, 1, "Course Title", text_top_style)
        # sheet.write(1, 2, "tes1")
        # sheet.merge_range(2, 0, 2, 1, "Level", text_top_style)
        # sheet.write(2, 2, "ea")
        # sheet.merge_range(3, 0, 3, 1, "Responsible", text_top_style)
        # sheet.write(3, 2, "tes2")
 
        row = 5
        sheet.freeze_panes(6, 10)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 9, 15)
        header = ['No.', 'Session', 'Instructor', 'Start Date', 'End Date', 'Duration', 'Seats', 'Attendees', 'Taken Seats(%)', 'Status']
        sheet.write_row(row, 0, header, text_header_style)
         
        no_list = []
        session = []
        partner = []
        start_date = []
        end_date = []
        duration = []
        seats = []
        attendees = []
        taken_seats = []
        status = []
 
        no = 1