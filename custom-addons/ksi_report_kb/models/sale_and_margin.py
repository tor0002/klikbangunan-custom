# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from datetime import datetime, time, timedelta, timezone, tzinfo
import pytz
import tzlocal
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell

class KsiReportKbSaleMargin(models.Model):
    _name = 'ksi.report.kb.sale.margin'
    _description = 'KSI Report KB - Sales & Margin'

    # _rec_name = 'name'
    # _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        # copy=False
    )
    
    date_start = fields.Date('Date Start')
    date_finish = fields.Date('Date Finish')
    company_id = fields.Many2one('res.company', string='Company')
    description = fields.Text()

    sale_margin_line_ids = fields.One2many('ksi.report.kb.sale.margin.line', 'sale_margin_id', string='Sale Margin Line')

    def generate_line(self):
        # pass
        
        for rec in self:
            if not rec.date_start or not rec.date_finish:
                return {
                    'warning': {
                        'title': 'Error Generating Line...',
                        'message': 'Date Start or Date Finish cannot be empty!'
                    }
                }

            date_from = datetime.combine(rec.date_start, time.min)
            date_until = datetime.combine(rec.date_finish, time.max)
            company_id = rec.company_id.id if rec.company_id else 0
            
            user = rec.env.user
            tz = pytz.timezone(user.tz) if user.tz else pytz.utc
            
            tz_region = tz.zone
            # print("TIME ZONE >>>", tz_region)
            
            
            # >>> START
            start = date_from
            ran = pytz.utc.localize(start).astimezone(tz)
            
            tz_start_region = ran.tzinfo.zone
            # print("TZ START REGION >>>", tz_start_region)
            
            start_date = ran.strftime("%d-%m-%Y %H:%M:%S")
            # print("START_DATE", start_date) #tanggal mulai real
            
            
            # FINISH <<<
            finish = date_until
            rin = pytz.utc.localize(finish).astimezone(tz)
            
            tz_finish_region = rin.tzinfo.zone
            # print("TZ FINISH REGION >>>", tz_finish_region)
            
            finish_date = rin.strftime("%d-%m-%Y %H:%M:%S")
            # print("FINISH_DATE", finish_date) #tanggal selesai real
            
            
            date_from = date_from - timedelta(hours=7, minutes=0)
            date_until = date_until - timedelta(hours=7, minutes=0)
            # print(" >>>>> ", date_from)
            # print(" >>>>> ", date_until)
            
            
            sql = """
                    select 
                        date_trunc('day', pos.date_order AT TIME ZONE 'UTC' AT TIME ZONE %s) as day_time,
                        count(distinct pol.order_id) as trans_num,
                        round(sum(pol.qty), 2) as qty_num,
                        --(select sum(pol.qty) from pos_order_line pol where pol.order_id=pos.id) "Quantity"
                        round(sum(pol.price_unit*qty), 2) as gross_value,
                        round(sum(pol.price_subtotal), 2) as sale_value,
                        round(sum(pol.price_subtotal_incl - pol.price_subtotal), 2) as tax_value,
                        round(sum(pol.price_subtotal_incl), 2) as net_sale_tax,
                        round(sum(pol.total_cost), 2) as cost_value,
                        round(sum(pol.price_subtotal - pol.total_cost), 2) as profit_value,
                        round(sum(pol.price_subtotal_incl - pol.total_cost), 2) as gross_margin_absolute,
                        (CASE
                            WHEN sum(pol.price_subtotal) > 0 THEN round(sum(pol.price_subtotal - pol.total_cost) / sum(pol.price_subtotal) * 100, 2)
                            ELSE 0
                        END) as percentage_margin
                    -- 	,
                    -- 	com.name "Company"
                    -- 	(select com.name from res_company com where pos.company_id = com.id)
                    from 
                        pos_order pos
                    join
                        pos_order_line pol on pos.id = pol.order_id
                    -- join
                    -- 	res_company com on pos.company_id = com.id 
                    where
                      pos.date_order >= %s and pos.date_order <= %s
                """
            
            cr = rec.env.cr
            
            if company_id==0:
                sql += """
                            --    and pos.state in ('done', 'paid', 'invoiced')
                            group by 1 --pos.id, pos.date_order::date
                            order by 1 --pos.date_order asc;
                        """
                cr.execute(sql, (tz_region, date_from, date_until))
                # cr.execute(sql, (tz_start_region, date_from, tz_finish_region, date_until))
            else:
                sql += """
                                and pos.company_id = %s
                            --    and pos.state in ('done', 'paid', 'invoiced')
                            group by 1 --pos.id, pos.date_order::date
                            order by 1 --pos.date_order asc;
                        """
                # cr.execute(sql, (date_from, date_until, company_id))
                cr.execute(sql, (tz_region, date_from, date_until, company_id))
            
            res = cr.dictfetchall()

            sm_line = [(5, 0, 0)]
            
            if res:
                # print ("RES BERISI: sql !!!", res)
                
                count = 1
                for r in res:
                    # print("trans_num", r['trans_num'])
                    value = {
                        'name'              : str(count).zfill(5), #r['name'],
                        'day_time'          : r['day_time'], #pytz.timezone(tz_start_region).localize(r['day_time']).astimezone(pytz.utc), #pytz.utc.localize(r['day_time']).astimezone(tz), #r['date_order'],
                        'trans_num'         : r['trans_num'], #len(rec.env['pos.order'].search([('date_order', '>=', datetime.combine(r['day_time'], time.min)), ('date_order', '<=', datetime.combine(r['day_time'], time.max))])), #r['trans_num'], #trans_num,
                        'qty_num'           : r['qty_num'], #qty_num,
                        'gross_value'       : r['gross_value'],
                        'sale_value'        : r['sale_value'], #r['amount_total']-r['amount_tax'],
                        'tax_value'         : r['tax_value'], #r['amount_tax'],
                        'net_sale_tax'      : r['net_sale_tax'], #r['amount_total'],
                        'cost_value'        : r['cost_value'],
                        'profit_value'      : r['profit_value'],
                        'gross_margin'      : r['gross_margin_absolute'],
                        'percentage_margin' : r['percentage_margin']
                    }
       
                    if False: #len(sm_line.search([('day_time', '=', r['date_order'])])) > 0:
                        pass
                    else:
                        sm_line.append((0, 0, value))
                        
                    count += 1
            else:
                pass
                # print("RES KOSONG: sql !!!")
            
            rec.sale_margin_line_ids = sm_line
    
    # @api.onchange('date_start', 'date_finish')
    # def _onchange_field(self):
    #     if self.date_start and self.date_finish:
    #         self.generate_line()
    #     else:
    #         return {
    #             'warning': {
    #                 'title': 'Error Generating Line...',
    #                 'message': 'Date Start and Date Finish cannot be empty!'
    #             }
    #         }

    def action_print(self):
        # for record in self:
        #     record.write({'name': 'value'})
        # return True
    
        return self.env.ref('ksi_report_kb.report_kb_sales_and_margin').report_action(self) 
    
    # @api.multi
    # def action_print(self):
    #     for record in self:
    #         template_report = 'ksi_report_kb.sale_margin'
    #         return record.env.ref(template_report).report_action(self)
    
    def get_excel_report(self):
        # redirect to /xlsx_reports controller to generate the excel file
        return {
            'type': 'ir.actions.act_url',
            'url': '/xlsx_reports/%s' % (self.id),
            'target': 'new',
        }
    
    def action_reset(self):
        for rec in self:
            rec.write({
                    'date_start': False,
                    'date_finish': False,
                    'company_id': False,
                    'sale_margin_line_ids': [(5, 0, 0)]
                })
    
class KsiReportKbSaleMarginLine(models.Model):
    _name = 'ksi.report.kb.sale.margin.line'
    _description = 'KSI Report KB - Sales & Margin Line'

    # _rec_name = 'name'
    # _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        # copy=False
    )
    
    day_time = fields.Datetime('Day')
    trans_num = fields.Integer('Trans')
    qty_num = fields.Float('Quantity', digits='Product Unit of Measure', default=0)
    gross_value = fields.Float('Gross')
    sale_value = fields.Float('Sales')
    tax_value = fields.Float('Tax Value')
    net_sale_tax = fields.Float('Net Sales + Tax')
    cost_value = fields.Float('Cost')
    profit_value = fields.Float('Profit')
    gross_margin = fields.Float('Gross Margin Absolute (in Rupiah)')
    percentage_margin = fields.Float('Margin (in percentage [%])')
    
    description = fields.Text()

    sale_margin_id = fields.Many2one('ksi.report.kb.sale.margin', string='Sale Margin', 
        ondelete='cascade'
    )
    
    # @api.multi
    def action_print(self):
        for record in self:
            record.write({'name': 'value'})
        return True


class KsiReportKbSaleMarginXlsx(models.AbstractModel):
    _name = 'report.ksi_report_kb.sale_margin_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, package):
        
        # print("===========> DATA", data)
        # print("===========> PACKAGE", package)
        
        for obj in package:
            report_name = obj.name
            
            # One sheet by package
            sheet = workbook.add_worksheet(report_name[:31])
            
            text_title_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'black', 'bg_color': 'yellow', 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
            bold = workbook.add_format({'bold': True, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
            border = workbook.add_format({'border': 1})
            text_header_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'white', 'bg_color': '#254dbe', 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
            text_style = workbook.add_format({'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
            number_style = workbook.add_format({'num_format': '#,##0', 'font_size': 12, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'border': 1})
            
            sheet.write(1, 2, 'TITLE', text_title_style)
            sheet.write(1, 3, obj.name, bold)
            sheet.write(1, 4, 'PERIOD', text_title_style)
            sheet.write(1, 5, ('%s - %s') % (obj.date_start.strftime('%d/%m/%Y'), obj.date_finish.strftime('%d/%m/%Y')), bold)
            sheet.write(1, 6, 'COMPANY', text_title_style)
            sheet.write(1, 7, obj.company_id.name if obj.company_id else 'All', bold)
            
            row = 3
            # sheet.freeze_panes(3, 10)
            sheet.set_column(0, 0, 5)
            sheet.set_column(1, 15, 25)
            header = ['No.', 'Day', 'Trans.', 'Quantity', 'Gross', 'Sales', 'Tax Value', 'Net. Sales + Tax', 'Cost', 'Profit', 'Gross Margin Absolute (Rp.)', '(%) Margin']
            # header = ['Day', 'Trans.', 'Quantity', 'Gross', 'Sales', 'Tax Value', 'Net. Sales + Tax', 'Cost', 'Gross Margin Absolute (Rp.)', '(%) Margin']
            sheet.write_row(row, 0, header, text_header_style)
            
            no = 1
            total_trans = total_qty = total_gross = total_sale = total_tax = total_sale_tax = total_cost = total_profit = total_margin = total_percentage = 0
            for x in obj.sale_margin_line_ids:
                list = []
                list.append(x.name)
                list.append(x.day_time.strftime('%d/%m/%y %-H:%M') if x.day_time else '#NAME?')
                list.append(x.trans_num or 0)
                list.append(x.qty_num or 0)
                list.append(x.gross_value or 0)
                list.append(x.sale_value or 0)
                list.append(x.tax_value or 0)
                list.append(x.net_sale_tax or 0)
                list.append(x.cost_value or 0)
                list.append(x.profit_value or 0)
                list.append('Rp.'+str(x.gross_margin).replace(".0", "")+',-' or 'Rp.0,-')
                list.append(str(x.percentage_margin) + "%" or '0%')

                total_trans += x.trans_num
                total_qty += x.qty_num
                total_gross += x.gross_value
                total_sale += x.sale_value
                total_tax += x.tax_value
                total_sale_tax += x.net_sale_tax
                total_cost += x.cost_value
                total_profit += x.profit_value
                total_margin += x.gross_margin
                total_percentage += x.percentage_margin
                
                no+=1
                
                row += 1
                
                sheet.write_row(row, 0, list, text_style)
            
            row+=1
            list = []
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            list.append("")
            sheet.write_row(row, 0, list, text_style)
            
            row+=1
            sheet.write(row, 0, '', border)
            sheet.write(row, 1, 'Total', bold)
            list = []
            list.append(total_trans)
            list.append(total_qty)
            list.append(total_gross)
            list.append(total_sale)
            list.append(total_tax)
            list.append(total_sale_tax)
            list.append(total_cost)
            list.append(total_profit)
            list.append('Rp.'+str(total_margin).replace(".0", "")+',-')
            list.append(str(round(total_percentage/no, 2))+'%' if no>0 else '0%')
            
            sheet.write_row(row, 2, list, number_style)
            
            print("NO >>>", no)
            
            no -= 1
            row+=1
            sheet.write(row, 0, '', border)
            sheet.write(row, 1, 'Avg', bold)
            list = []
            list.append(total_trans/no if no>0 else 0)
            list.append(total_qty/no if no>0 else 0)
            list.append(total_gross/no if no>0 else 0)
            list.append(total_sale/no if no>0 else 0)
            list.append(total_tax/no if no>0 else 0)
            list.append(total_sale_tax/no if no>0 else 0)
            list.append(total_cost/no if no>0 else 0)
            # list.append(total_profit/no if no>0 else 0)
            # list.append(total_margin/no if no>0 else 0)
            # list.append(total_percentage/no if no>0 else 0)
            
            sheet.write_row(row, 2, list, number_style)
            
            sheet.write(row, 9, '', border)
            sheet.write(row, 10, '', border)
            sheet.write(row, 11, '', border)
            