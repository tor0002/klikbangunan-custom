from odoo import _, api, fields, models


class HrPayslipInputType(models.Model):
    _inherit = 'hr.payslip.input.type'

    is_otomatic = fields.Boolean('Otomatic')


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def recompute_worked_day_lines(self):
        self._compute_worked_days_line_ids()

    @api.onchange('struct_id')
    def onchange_struct_id(self):
        lines = [(5, 0, 0)]
        for line in self.struct_id.input_line_type_ids:
            val = {
                'input_type_id': line.id,
                'name': line.name,
                'amount': 0.0,
            }
            lines.append((0, 0, val))
        self.input_line_ids = lines

    def compute_sheet(self):
        self.recompute_worked_day_lines()
        res = super(HrPayslip, self).compute_sheet()

        return res

    @api.model_create_multi
    def create(self, vals):
        self.onchange_struct_id()
        res = super(HrPayslip, self).create(vals)
        return res

    def _get_worked_day_lines_values(self, domain=None):
        self.ensure_one()
        res = []
        hours_per_day = self._get_worked_day_lines_hours_per_day()
        work_hours = self.contract_id._get_work_hours(self.date_from, self.date_to, domain=domain)
        work_hours_ordered = sorted(work_hours.items(), key=lambda x: x[1])
        biggest_work = work_hours_ordered[-1][0] if work_hours_ordered else 0
        add_days_rounding = 0
        for work_entry_type_id, hours in work_hours_ordered:
            work_entry_type = self.env['hr.work.entry.type'].browse(work_entry_type_id)
            days = round(hours / hours_per_day, 5) if hours_per_day else 0
            
            if work_entry_type_id == biggest_work:
                days += add_days_rounding
            day_rounded = self._round_days(work_entry_type, days)
            add_days_rounding += (days - day_rounded)


            # ! custom
            count_we = self.env['hr.work.entry'].search_count([
                ('employee_id', '=', self.employee_id.id),
                ('work_entry_type_id', '=', work_entry_type_id)
            ])

            attendance_line = {
                'sequence': work_entry_type.sequence,
                'work_entry_type_id': work_entry_type_id,
                'number_of_days': day_rounded,
                'number_of_hours': hours,
                'count' : count_we if count_we else 0
            }
            res.append(attendance_line)
        return res


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    @api.onchange('structure_id')
    def onchange_structure_id(self):
        type = self.structure_id.type_id
        contracts = self.env['hr.contract'].search(
            [('state', '=', 'open'), ('structure_type_id', '=', type.id)])
        lines = [(5, 0, 0)]
        
        for line in contracts:
            val = {
                'name': line.employee_id.name,
                'work_email': line.employee_id.work_email,
                'department_id': line.department_id.id,
            }
            lines.append((4, line.employee_id.id, val))
        self.employee_ids = lines

class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    count = fields.Float('Count')
    
