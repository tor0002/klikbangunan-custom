from odoo import fields, models, api, _

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    from odoo.addons.setu_advance_inventory_reports.library import xlsxwriter
from . import setu_excel_formatter
import base64
from io import BytesIO


class SetuInventoryCoverageReport(models.TransientModel):
    _name = 'setu.inventory.coverage.report'
    _description = """Setu Inventory Coverage Report """

    stock_file_data = fields.Binary('Stock Movement File')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    company_ids = fields.Many2many("res.company", string="Companies")
    product_category_ids = fields.Many2many("product.category", string="Product Categories")
    product_ids = fields.Many2many("product.product", string="Products")
    warehouse_ids = fields.Many2many("stock.warehouse", string="Warehouses")
    report_by = fields.Selection([('company', 'Company'), ('warehouse', 'Warehouse')], default='warehouse')
    internal_transfers_as_sales = fields.Boolean(string="Consider Internal Warehouse Transfer As Sales")

    @api.onchange('product_category_ids')
    def onchange_product_category_id(self):
        if self.product_category_ids:
            return {'domain': {'product_ids': [('categ_id', 'child_of', self.product_category_ids.ids)]}}

    @api.onchange('company_ids')
    def onchange_company_id(self):
        if self.company_ids:
            return {'domain': {'warehouse_ids': [('company_id', 'child_of', self.company_ids.ids)]}}

    @api.onchange('report_by')
    def onchange_report_by(self):
        if self.report_by == 'company':
            self.internal_transfers_as_sales = False

    def get_file_name(self):
        filename = "inventory_coverage_report.xlsx"
        return filename

    def create_excel_workbook(self, file_pointer):
        workbook = xlsxwriter.Workbook(file_pointer)
        return workbook

    def create_excel_worksheet(self, workbook, sheet_name):
        worksheet = workbook.add_worksheet(sheet_name)
        worksheet.set_default_row(22)
        # worksheet.set_border()
        return worksheet

    def set_column_width(self, workbook, worksheet):
        worksheet.set_column(0, 1, 25)
        worksheet.set_column(2, 10, 14)

    def set_format(self, workbook, wb_format):
        wb_new_format = workbook.add_format(wb_format)
        wb_new_format.set_border()
        return wb_new_format

    def set_report_title(self, workbook, worksheet):
        wb_format = self.set_format(workbook, setu_excel_formatter.FONT_TITLE_CENTER)
        worksheet.merge_range(0, 0, 1, 10, "Inventory Coverage Report", wb_format)
        wb_format_left = self.set_format(workbook, setu_excel_formatter.FONT_MEDIUM_BOLD_LEFT)
        wb_format_center = self.set_format(workbook, setu_excel_formatter.FONT_MEDIUM_BOLD_CENTER)

        worksheet.write(2, 0, "Sales Start Date", wb_format_left)
        worksheet.write(3, 0, "Sales End Date", wb_format_left)

        wb_format_center = self.set_format(workbook, {'num_format': 'dd/mm/yy', 'align': 'center', 'bold': True,
                                                      'font_color': 'red'})
        worksheet.write(2, 1, self.start_date, wb_format_center)
        worksheet.write(3, 1, self.end_date, wb_format_center)

    def get_inventory_coverage_report_data(self, for_reporting=False):
        """
        :return:
        """
        start_date = self.start_date
        end_date = self.end_date
        category_ids = company_ids = {}
        if self.product_category_ids:
            categories = self.env['product.category'].search([('id', 'child_of', self.product_category_ids.ids)])
            category_ids = set(categories.ids) or {}
        products = self.product_ids and set(self.product_ids.ids) or {}

        if self.company_ids:
            companies = self.env['res.company'].search([('id', 'child_of', self.company_ids.ids)])
            company_ids = set(companies.ids) or {}
        else:
            company_ids = set(self.env.context.get('allowed_company_ids', False) or self.env.user.company_ids.ids) or {}

        warehouses = self.warehouse_ids and set(self.warehouse_ids.ids) or {}
        include_internal_transfer = 'Y' if self.internal_transfers_as_sales else False
        query = """
                       Select * from get_inventory_coverage_data('%s','%s','%s','%s','%s','%s','%s','%d','%s')
                   """ % (
            company_ids, products, category_ids, warehouses, start_date, end_date, self.report_by, self.id,
            include_internal_transfer)
        self._cr.execute(query)
        stock_data = self._cr.dictfetchall()
        if for_reporting:
            self._cr.execute(f"""select * from setu_inventory_coverage_analysis_bi_report where wizard_id={self.id}""")
            stock_data = self._cr.dictfetchall()
            return stock_data
        return stock_data

    def prepare_data_to_write(self, stock_data={}):
        """

        :param stock_data:
        :return:
        """
        company_wise_data = {}
        for data in stock_data:
            key = (data.get('company_id'), data.get('company_name'))
            if not company_wise_data.get(key, False):
                company_wise_data[key] = {data.get('product_id'): data}
            else:
                company_wise_data.get(key).update({data.get('product_id'): data})
        return company_wise_data

    def download_report(self):
        file_name = self.get_file_name()
        file_pointer = BytesIO()
        stock_data = self.get_inventory_coverage_report_data(for_reporting=True)
        company_wise_analysis_data = self.prepare_data_to_write(stock_data=stock_data)
        if not company_wise_analysis_data:
            return False
        workbook = self.create_excel_workbook(file_pointer)
        for stock_data_key, stock_data_value in company_wise_analysis_data.items():
            sheet_name = stock_data_key[1]
            wb_worksheet = self.create_excel_worksheet(workbook, sheet_name)
            row_no = 3
            self.write_report_data_header(workbook, wb_worksheet, row_no)
            for age_data_key, age_data_value in stock_data_value.items():
                row_no = row_no + 1
                self.write_data_to_worksheet(workbook, wb_worksheet, age_data_value, row=row_no)

        # workbook.save(file_name)
        workbook.close()
        file_pointer.seek(0)
        file_data = base64.b64encode(file_pointer.read())
        self.write({'stock_file_data': file_data})
        file_pointer.close()

        return {
            'name': 'Inventory Coverage Report',
            'type': 'ir.actions.act_url',
            'url': '/web/content?model=setu.inventory.coverage.report&field=stock_file_data&id=%s&filename=%s' % (
                self.id, file_name),
            'target': 'new',
        }

    def download_report_in_listview(self):
        coverage_data = self.get_inventory_coverage_report_data()
        graph_view_id = self.env.ref(
            'setu_advance_inventory_reports.setu_inventory_coverage_analysis_bi_report_graph').id
        tree_view_id = self.env.ref(
            'setu_advance_inventory_reports.setu_inventory_coverage_analysis_bi_report_tree').id
        is_graph_first = self.env.context.get('graph_report', False)
        context = self._context.copy() or {}
        context.update({'icr_report_by': self.report_by})
        report_display_views = []
        viewmode = ''
        if is_graph_first:
            report_display_views.append((graph_view_id, 'graph'))
            report_display_views.append((tree_view_id, 'tree'))
            viewmode = "graph,tree"
        else:
            report_display_views.append((tree_view_id, 'tree'))
            report_display_views.append((graph_view_id, 'graph'))
            viewmode = "tree,graph"
        return {
            'name': _('Inventory Coverage Analysis'),
            'domain': [('wizard_id', '=', self.id)],
            'res_model': 'setu.inventory.coverage.analysis.bi.report',
            'view_mode': viewmode,
            'type': 'ir.actions.act_window',
            'context': context,
            'views': report_display_views,
        }

    # def create_data(self, data):
    #     del data['company_name']
    #     del data['product_name']
    #     del data['category_name']
    #     return self.env['setu.inventory.coverage.analysis.bi.report'].create(data)

    def write_report_data_header(self, workbook, worksheet, row):
        self.set_report_title(workbook, worksheet)
        self.set_column_width(workbook, worksheet)
        worksheet.set_row(row, 28)
        wb_format = self.set_format(workbook, setu_excel_formatter.FONT_MEDIUM_BOLD_CENTER)
        wb_format.set_text_wrap()
        worksheet.set_row(row, 30)
        odd_normal_right_format = self.set_format(workbook, setu_excel_formatter.ODD_FONT_MEDIUM_BOLD_RIGHT)
        even_normal_right_format = self.set_format(workbook, setu_excel_formatter.EVEN_FONT_MEDIUM_BOLD_RIGHT)
        normal_left_format = self.set_format(workbook, setu_excel_formatter.FONT_MEDIUM_BOLD_LEFT)
        odd_normal_right_format.set_text_wrap()
        even_normal_right_format.set_text_wrap()
        normal_left_format.set_text_wrap()

        worksheet.write(row, 0, 'Company', normal_left_format)
        worksheet.write(row, 1, 'Product', normal_left_format)
        worksheet.write(row, 2, 'Category', odd_normal_right_format)
        column_no = 3
        if self.report_by == 'warehouse':
            worksheet.write(row, column_no, 'Warehouse', even_normal_right_format)
            column_no += 1
        worksheet.write(row, column_no, 'Current Stock', odd_normal_right_format)
        worksheet.write(row, column_no + 1, 'Average Daily Sales', even_normal_right_format)
        worksheet.write(row, column_no + 2, 'Coverage Days', odd_normal_right_format)
        return worksheet

    def write_data_to_worksheet(self, workbook, worksheet, data, row):
        # Start from the first cell. Rows and
        # columns are zero indexed.
        odd_normal_right_format = self.set_format(workbook, setu_excel_formatter.ODD_FONT_MEDIUM_NORMAL_RIGHT)
        even_normal_right_format = self.set_format(workbook, setu_excel_formatter.EVEN_FONT_MEDIUM_NORMAL_RIGHT)
        even_normal_center_format = self.set_format(workbook, setu_excel_formatter.EVEN_FONT_MEDIUM_NORMAL_CENTER)
        odd_normal_center_format = self.set_format(workbook, setu_excel_formatter.ODD_FONT_MEDIUM_NORMAL_CENTER)
        odd_normal_left_format = self.set_format(workbook, setu_excel_formatter.ODD_FONT_MEDIUM_NORMAL_LEFT)
        normal_left_format = self.set_format(workbook, setu_excel_formatter.FONT_MEDIUM_NORMAL_LEFT)

        worksheet.write(row, 0, data.get('company_name', ''), normal_left_format)
        worksheet.write(row, 1, data.get('product_name', ''), normal_left_format)
        worksheet.write(row, 2, data.get('category_name', ''), odd_normal_right_format)
        column_no = 3
        if self.report_by == 'warehouse':
            worksheet.write(row, column_no, data.get('warehouse_name', ''), even_normal_right_format)
            column_no += 1
        worksheet.write(row, column_no, data.get('current_stock', ''), odd_normal_right_format)
        worksheet.write(row, column_no + 1, data.get('average_daily_sales', ''), even_normal_right_format)
        worksheet.write(row, column_no + 2, data.get('coverage_days', ''), odd_normal_center_format)
        return worksheet


class SetuABCXYZAnalysisBIReport(models.TransientModel):
    _name = 'setu.inventory.coverage.analysis.bi.report'
    _description = "It helps to manage abc-xyz analysis data in listview and graphview"

    product_id = fields.Many2one("product.product", "Product")
    product_category_id = fields.Many2one("product.category", "Category")
    company_id = fields.Many2one("res.company", "Company")
    warehouse_id = fields.Many2one("stock.warehouse")
    average_daily_sales = fields.Float("ADS")
    current_stock = fields.Float("Current Stock")
    coverage_days = fields.Integer("Coverage Days")
    company_name = fields.Char("Company")
    product_name = fields.Char("Product")
    category_name = fields.Char("Category")
    warehouse_name = fields.Char("Warehouse")
    wizard_id = fields.Many2one("setu.inventory.coverage.report")
