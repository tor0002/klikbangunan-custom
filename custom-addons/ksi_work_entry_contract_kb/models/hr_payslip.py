import base64
import logging

from collections import defaultdict
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, Command, fields, models, _
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips, ResultRules
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round, date_utils, convert_file, html2plaintext
from odoo.tools.float_utils import float_compare
from odoo.tools.misc import format_date
from odoo.tools.safe_eval import safe_eval

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
    def _compute_worked_days_line_ids(self):
        if self.env.context.get('salary_simulation'):
            return
        valid_slips = self.filtered(lambda p: p.employee_id and p.date_from and p.date_to and p.contract_id and p.struct_id)
        # Make sure to reset invalid payslip's worked days line
        invalid_slips = self - valid_slips
        invalid_slips.worked_days_line_ids = [(5, False, False)]
        # Ensure work entries are generated for all contracts
        generate_from = min(p.date_from for p in self)
        current_month_end = date_utils.end_of(fields.Date.today(), 'month')
        generate_to = max(min(fields.Date.to_date(p.date_to), current_month_end) for p in self)

        # ! disable automatic work entries
        # self.mapped('contract_id')._generate_work_entries(generate_from, generate_to)

        for slip in valid_slips:
            slip.write({'worked_days_line_ids': slip._get_new_worked_days_lines()})
