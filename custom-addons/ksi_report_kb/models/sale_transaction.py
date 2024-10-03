# -*- coding: utf-8 -*-

import calendar
import pytz

from odoo import _, api, fields, models
from odoo.tools import float_is_zero
# from datetime import datetime, time, timedelta
# from dateutil.relativedelta import relativedelta
from dateutil import rrule

# from xlsxwriter.utility import xl_range
# from xlsxwriter.utility import xl_rowcol_to_cell

# Ref:
# actionButtonStrings
# actionItems

# https://learnopenerp.blogspot.com/2019/03/how-to-hide-export-option-from-more-menu-in-odoo.html
# https://www.youtube.com/watch?v=zbeBTImPKUw

class KsiReportKbSaleTransaction(models.Model):
    _name = 'ksi.report.kb.sale.transaction'
    _description = 'KSI Report KB - Sale Transaction'

    # _rec_name = 'name'
    _order = 'year ASC, month ASC, company_id ASC'

    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        # copy=False
    )
    
    company_id = fields.Many2one('res.company', string='Company')
    company_code = fields.Char('Company', compute='_compute_company_code', store=True)
    
    month = fields.Integer('Month')
    year = fields.Integer('Year')
    
    month_name = fields.Char('Month', compute='_compute_month_name', store=True)
    year_name = fields.Char('Year', compute='_compute_year_name', store=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id, required=True, readonly=True)
    
    actual = fields.Float('Actual', digits=(16,2), default=0.0, group_operator="sum") #, group_operator=False
    # actual_sum = fields.Float('Actual (Sum)', digits=(16,2), compute='_compute_actual_sum', store=True, group_operator="sum")
    actual_avg = fields.Float('Actual (Avg)', digits=(16,2), compute='_compute_actual_avg', store=True, group_operator="avg")
    
    target = fields.Float('Target', digits=(16,2), default=0.0, group_operator="sum") #, group_operator=False
    # target_sum = fields.Float('Target (Sum)', digits=(16,2), compute='_compute_target_sum', store=True, group_operator="sum")
    target_avg = fields.Float('Target (Avg)', digits=(16,2), compute='_compute_target_avg', store=True, group_operator="avg")
    
    percent = fields.Float('Percent (%)', digits=(12,2), compute='_compute_percent', store=True)
    
    description = fields.Text()
    
    # sale_transaction_line_ids = fields.One2many('ksi.report.kb.sale.transaction.line', 'sale_transaction_id', string='Sale Transaction Line')
    
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     print("FIELDS VIEW GET !!!", view_id)
    #     if toolbar:
    #         print("IF TOOLBAR !!!", toolbar, res['toolbar'])
    #         for action in res['toolbar'].get('action'):
    #             print("FOR ACTION !!!")
    #             if action.get('xml_id'):
    #                 print("GET XML ID !!!")
    #                 if action['xml_id'] == 'ksi_report_kb_sale_transaction_action' and self._context.get('default_type') == 'entry':
    #                     res['toolbar']['action'].remove(action)
        
    #     return res

    @api.depends('company_id')
    def _compute_company_code(self):
        for rec in self:
            rec.company_code = rec.company_id.warehouse_id.code
            
    @api.depends('month')
    def _compute_month_name(self):
        for rec in self:
            rec.month_name = calendar.month_name[rec.month]
    
    @api.depends('year')
    def _compute_year_name(self):
        for rec in self:
            rec.year_name = str(rec.year)
    
    @api.depends('actual')
    def _compute_actual_sum(self):
        for rec in self:
            rec.actual_sum = rec.actual
            
    @api.depends('actual')
    def _compute_actual_avg(self):
        for rec in self:
            rec.actual_avg = rec.actual
            
    @api.depends('target')
    def _compute_target_sum(self):
        for rec in self:
            rec.target_sum = rec.target
            
    @api.depends('target')
    def _compute_target_avg(self):
        for rec in self:
            rec.target_avg = rec.target
            
    def generate(self):
        # print("CONTEXT", self.env.context)
        
        # active_company_ids = self._context.get('allowed_company_ids')
        
        # selected_companies = self.env['res.company'].browse(active_company_ids)
        # print("COMPANIES >>>>>", selected_companies)
        
        user = self.env.user
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        
        tz_region = tz.zone
        # print("TIME ZONE >>>", tz_region)
        
        sql = """ 
                SELECT 
                    date_trunc('month', date_order AT TIME ZONE 'UTC' AT TIME ZONE %s) AS txn_month, 
                    company_id,
                    round(sum(amount_total), 2) as monthly_sum
                FROM 
                    pos_order
                --WHERE 
                    --company_id IN
            """
        
        # sql += """("""
        # no = 1
        # for c in active_company_ids:
        #     sql += str(c)
        #     if no<len(active_company_ids):
        #         sql += ','
        #         no += 1
        #     else:
        #         sql += """)"""
                    
        sql += """ 
                GROUP BY 
                    txn_month,
                    company_id
                ORDER BY
                    txn_month,
                    company_id
            """
        
        cr = self.env.cr
        cr.execute(sql, [tz_region])
        res = cr.dictfetchall()

        # st_line = [(5, 0, 0)]
        
        if res:
            print ("RES BERISI: sql !!!", res)
            print ("RES PERTAMA: sql !!!", res[0])
            print ("RES TERAKHIR: sql !!!", res[-1])
            
            # dates
            start_date = res[0].get('txn_month')
            finish_date = res[-1].get('txn_month')
            
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=finish_date):
                ada = True
                # if any(s['txn_month'] == dt for s in res):
                #     # data exists
                #     ada = True
                #     print("ADA !!!")
                
                for c in self.env['res.company'].search([], order="id ASC"):
                    sale_transaction = self.env['ksi.report.kb.sale.transaction'].sudo().search([('year', '=', dt.year), ('month', '=', dt.month), ('company_id', '=', c.id)], limit=1)
                    if not sale_transaction:
                        ada = False
                        # c_code = c.warehouse_id.code if c.warehouse_id.code else ''
                        name = str(dt.year) + '#' + str(dt.month).zfill(2) + '#' + c.name.replace(' ', '')
                        vals = {
                            'name'      : name,
                            'year'      : dt.year,
                            'month'     : dt.month,
                            'company_id': c.id
                        }
                        self.env['ksi.report.kb.sale.transaction'].sudo().create(vals)
                print(dt, ada)
            
            for r in res:
                sale_transaction = self.env['ksi.report.kb.sale.transaction'].sudo().search([('year', '=', r['txn_month'].year), ('month', '=', r['txn_month'].month), ('company_id', '=', r['company_id'])], limit=1)
                if sale_transaction:
                    vals = {
                        'actual'    : r['monthly_sum']
                    }
                    sale_transaction.sudo().write(vals)
        else:
            pass
            # print("RES KOSONG: sql !!!")

    @api.depends('target')
    def _compute_percent(self):
        for rec in self:
            # print("JUAN", float_is_zero(rec.target, precision_digits=rec.currency_id.decimal_places))
            if float_is_zero(rec.target, precision_digits=rec.currency_id.decimal_places) == 0:
                rec.percent = rec.actual / rec.target * 100.0
            else:
                rec.percent = 0.0
                
    def action_print(self):
        return self.env.ref('ksi_report_kb.report_kb_sale_transaction').report_action(self)
    
    def do_export(self):
        return self.env.ref('ksi_report_kb.report_kb_sale_transaction').report_action(self.env['ksi.report.kb.sale.transaction'])
    
    def clear_data(self):
        # print(" DATA CLEARANCE ")
        for data in self.env['ksi.report.kb.sale.transaction'].sudo().search([]):
            data.sudo().unlink()

class KsiReportKbSaleTransactionXlsx(models.AbstractModel):
    _name = 'report.ksi_report_kb.sale_transaction_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, package):
        
        print("===========> DATA", data)
        print("===========> PACKAGE", package) #, package.sorted(key=lambda r: (r.name, r.country_id.name))
        
        year_list = []
        month_list = []
        company_list = []
        
        sheet = workbook.add_worksheet("Sale Transaction")
        
        # formatting
        text_red = workbook.add_format({'bold': True, 'font_color': 'red', 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
        bold_border = workbook.add_format({'bold': True, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
        text_style = workbook.add_format({'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
        
        sale_transaction = self.env['ksi.report.kb.sale.transaction'].sudo().search([], order="year ASC, company_id ASC, month ASC")#.sorted(lambda r: (r.company_id,)) # r.year, r.month
        # print("SALE TRANSACTION", sale_transaction)
        
        for y in sale_transaction.mapped('year'):
            if y not in year_list:
                year_list.append(y)
        
        # print("YL", year_list)
        
        for c in sale_transaction.mapped('company_id'):
            if c.id not in company_list:
                company_list.append(c.id)
        
        # print("CL", company_list)
        
        for m in sale_transaction.mapped('month'):
            if m not in month_list:
                month_list.append(m)
        
        # print("ML", month_list)
        
        row = 0
        col = 0
        
        list = []
        atl = {'1': 0.0, '2': 0.0, '3': 0.0, '4': 0.0, '5': 0.0, '6': 0.0, '7': 0.0, '8': 0.0, '9': 0.0, '10': 0.0, '11': 0.0, '12': 0.0, '13': 0.0}
        tgt = {'1': 0.0, '2': 0.0, '3': 0.0, '4': 0.0, '5': 0.0, '6': 0.0, '7': 0.0, '8': 0.0, '9': 0.0, '10': 0.0, '11': 0.0, '12': 0.0, '13': 0.0}
        for yl in year_list:
            list = []
            row = 0
            
            list.append("Tahun " + str(yl))
            sheet.write_row(row, col, list, text_red)
            row += 1
            
            list = []
            list.append("BULAN")
            sheet.merge_range(row, col, row+1, col, 'BULAN', bold_border)
            row += 2
            
            for m in month_list:
                list = []
                list.append(calendar.month_name[m].upper())
                sheet.write_row(row, col, list, bold_border)
                row += 1
            
            list = []
            list.append("TOTAL")
            sheet.write_row(row, col, list, bold_border)
            row += 1
            list = []
            list.append("AVERAGE")
            sheet.write_row(row, col, list, bold_border)
            row += 1
            
            col += 1
            
            for cl in company_list:
                actual_sum_total = 0.0
                target_sum_total = 0.0
                count = 0
                row = 1
                
                res_com = self.env['res.company'].sudo().search([('id', '=', cl)], limit=1)
                # print("RES COM", res_com.name)
                list = []
                list.append(res_com.name.upper())
                sheet.merge_range(row, col, row, col+2, res_com.name, text_style)
                row += 1
                
                list = []
                list.append('ACTUAL')
                list.append('TARGET')
                list.append('%')
                sheet.write_row(row, col, list, text_style)
                row += 1
                
                for ml in month_list:
                    count += 1
                    list = []
                    sl_trx = self.env['ksi.report.kb.sale.transaction'].sudo().search([('year', '=', yl), ('company_id', '=', cl), ('month', '=', ml)], limit=1)
                    # print("SL TRX", sl_trx)
                    list.append(sl_trx.actual)
                    list.append(sl_trx.target)
                    current_margin = sl_trx.actual / sl_trx.target * 100 if sl_trx.target > 0.0 else 0.0
                    list.append(str(round(current_margin, 2)) + '%')
                    sheet.write_row(row, col, list, text_style)
                    
                    actual_sum_total += sl_trx.actual
                    target_sum_total += sl_trx.target
                    
                    atl[str(ml)] += sl_trx.actual
                    tgt[str(ml)] += sl_trx.target
                    
                    row += 1

                list = []
                # print("TOTAL", actual_sum_total, target_sum_total, actual_sum_total/target_sum_total if target_sum_total > 0.0 else 0.0)
                list.append(actual_sum_total)
                list.append(target_sum_total)
                list.append(str(round(actual_sum_total/target_sum_total, 2)) + '%' if target_sum_total > 0.0 else str(0.0) + '%')
                sheet.write_row(row, col, list, text_style)
                row += 1
                
                list = []
                # print("AVERAGE", actual_sum_total/count if count > 0 else 0.0, target_sum_total/count if count > 0 else 0.0)
                list.append(actual_sum_total/count if count > 0 else 0.0)
                list.append(target_sum_total/count if count > 0 else 0.0)
                list.append('')
                sheet.write_row(row, col, list, text_style)
                
                col += 3
        
        # print("ATL", atl)
        # print("TGT", tgt)
        
        row = 1
        
        sheet.merge_range(row, col, row, col+2, 'TOTAL', text_style)
        row += 1
        
        list = []
        list.append('ACTUAL')
        list.append('TARGET')
        list.append('%')
        sheet.write_row(row, col, list, text_style)
        row += 1
        
        actual_sum_total = 0.0
        target_sum_total = 0.0
        count = 0
        for r in range(1, 13):
            count += 1
            list = []
            act = atl[str(r)]
            tar = tgt[str(r)]
            mar = round(act/tar*100 - 100 if tar>0.0 else 0.0, 2)
            list.append(act)
            list.append(tar)
            list.append(str(mar))
            sheet.write_row(row, col, list, text_style)
            actual_sum_total += act
            target_sum_total += tar
            row += 1
        
        list = []
        tot_act = actual_sum_total
        list.append(tot_act)
        tot_tar = target_sum_total
        list.append(tot_tar)
        tot_mar = round(act/tar*100 - 100 if tar>0.0 else 0.0, 2)
        list.append(tot_mar)
        sheet.write_row(row, col, list, text_style)
        row += 1
        
        list = []
        ave_act = actual_sum_total/count if count>0 else 0.0 
        list.append(round(ave_act, 2))
        ave_tar = target_sum_total/count if count>0 else 0.0
        list.append(round(ave_tar, 2))
        ave_mar = '='
        list.append(ave_mar)
        sheet.write_row(row, col, list, text_style)
        row += 1
        