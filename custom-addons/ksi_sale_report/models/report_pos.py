from odoo import _, api, fields, models
import datetime
class ReportKsiPostReportReportPos(models.Model):
    _name = 'report.ksi_sale_report.report_sale'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        # ! if dia pilih month
        tuple_str_company = str(obj.company_ids.ids).replace("[", "(").replace("]", ")")
        tuple_str_sales = str(obj.crm_ids.ids).replace("[", "(").replace("]", ")")

        # ! ambil smua month
        sheet = workbook.add_worksheet('Course %s' % obj.group_by)
        text_top_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'white', 'bg_color': '#b904bf', 'valign': 'vcenter', 'text_wrap': True})
        # text_header_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'white', 'bg_color': '#b904bf', 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        text_center_style = workbook.add_format({'border':1,'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'shrink': True})
        text_style = workbook.add_format({'border':1,'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'align': 'left', 'shrink': True})
        number_style = workbook.add_format({'num_format': '#,##0', 'font_size': 12, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True})

        list_crm_name = []
        for crm in obj.crm_ids:
            list_crm_name.append(crm.name)

        sheet.merge_range(0, 0, 0, 1, "KLIKBANGUNAN")
        sheet.merge_range(1, 0, 1, 1, "PRODUCT MARGIN REPORT : " + ','.join(list_crm_name))
        sheet.merge_range(2, 0, 2, 1, "COMPANY :")
        # ! styling center number
        # sheet.set_column_pixels(6,6000, None, text_center_style)
        list_company_name = []
        for company in obj.company_ids:
            list_company_name.append(company.name)
        sheet.merge_range(3, 0, 3, 1, ','.join(list_company_name))
        sheet.merge_range('A5:A6', "No", text_center_style)
        sheet.merge_range('B5:B6', "Product Name", text_center_style)
 
        row = 5
        sheet.freeze_panes(6, 10)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 9, 15)
        sheet.set_column('B:B', 105)
        sheet.set_column('C:K', 15)


        header = ['No', 'Session', 'Instructor', 'Start Date', 'End Date','Duration', 'Seats', 'Attendees','Taken Seats(%)','Status']
        header = []
        # sheet.write_row(row, 0, header, text_header_style)
        
        sheet.merge_range("C5:E5", datetime.date(int(obj.year), int(obj.month), 1).strftime('%B - %Y'), text_center_style)
        sheet.write_row(5,2,['Total Price','Total Margin','Margin %'], text_style)

        self.env.cr.execute(
            """
            WITH product_per_month AS (
                SELECT
                    product_id AS product_id,
                    pt.name AS product_name,
                    pt.default_code AS default_code,
                    SUM(price_total) AS total_price,
                    SUM(margin) AS total_margin,
                    pt.priority AS priority,
                    date_trunc('month', timezone('Asia/Bangkok', timezone('UTC',sr.date))::timestamp) AS month_filter
                FROM 
                    sale_report AS sr
                LEFT JOIN
                    product_product AS pp ON pp.id = sr.product_id
                LEFT JOIN
                    product_template AS pt ON pt.id = pp.product_tmpl_id
                LEFT JOIN
                    crm_team AS ct ON ct.id = sr.team_id
                WHERE ("sr"."company_id" IS NULL  
                    OR ("sr"."company_id" in {company}))
                    AND ct.id in {sales}
                GROUP BY
                    product_id,
                    product_name,
                    pt.priority,
                    pt.default_code,
                    month_filter
                ORDER BY
                    pt.priority DESC,
                    pt.default_code
            ), product_month AS (
                    SELECT 
                        product_id,
                        product_name,
                        default_code,
                        SUM(CASE WHEN month_filter = '{year}-{month}-01 00:00:00' THEN total_price END) AS total_price,
                        SUM(CASE WHEN month_filter = '{year}-{month}-01 00:00:00' THEN total_margin END) AS total_margin
                    FROM 
                        product_per_month AS ppm
                    GROUP BY 
                        product_id,
                        product_name,
                        priority,
                        default_code
                    ORDER BY
                        priority DESC,
                        default_code
                )
                SELECT 
                    product_id,
                    product_name,
                    default_code,
                    total_price,
                    total_margin,
                    CASE WHEN total_price > 0 THEN total_margin / total_price * 100 END AS margin_percent
                FROM product_month
            """.format(month=obj.month, year=obj.year, company=tuple_str_company, sales=tuple_str_sales)
        )
        data_record = self.env.cr.dictfetchall()
        no_list = 1
        no = 1
        row = 6
        for p in data_record:
           
            data_row = [
                no,
                "[%s] %s" % (p['default_code'], p['product_name']),
                p['total_price'] if p['total_price'] else '-',
                p['total_margin'] if p['total_margin'] else '-',
                "{} %".format(round(p['margin_percent'],2) if p['margin_percent'] else '-')
            ]
            sheet.write_row(row,     0, data_row , text_style)
            row+=1
            no += 1


    
        