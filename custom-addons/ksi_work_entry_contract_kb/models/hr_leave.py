from odoo import _, api, fields, models
from odoo.exceptions import UserError
class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.depends('holiday_type')
    def _compute_from_holiday_type(self):
        for holiday in self:
            if holiday.holiday_type == 'employee':
                if not holiday.employee_ids:
                    # This handles the case where a request is made with only the employee_id
                    # but does not need to be recomputed on employee_id changes
                    # holiday.employee_ids = holiday.employee_id or self.env.user.employee_id
                    holiday.employee_ids = False

                holiday.mode_company_id = False
                holiday.category_id = False
            elif holiday.holiday_type == 'company':
                holiday.employee_ids = False
                if not holiday.mode_company_id:
                    holiday.mode_company_id = self.env.company.id
                holiday.category_id = False
            elif holiday.holiday_type == 'department':
                holiday.employee_ids = False
                holiday.mode_company_id = False
                holiday.category_id = False
            elif holiday.holiday_type == 'category':
                holiday.employee_ids = False
                holiday.mode_company_id = False
            # else:
            #     holiday.employee_ids = self.env.context.get('default_employee_id') or holiday.employee_id or self.env.user.employee_id


    # @api.model
    # def default_get(self, fields):
    #     result = super(HrLeave, self).default_get(fields)

    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== result description ------->","result -> {}".format(result));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
    #     if "holiday_type" in result:
    #         del result['holiday_type']
    #     return result

    def _cancel_work_entry_conflict(self):
        return False
        # """
        # Creates a leave work entry for each hr.leave in self.
        # Check overlapping work entries with self.
        # Work entries completely included in a leave are archived.
        # e.g.:
        #     |----- work entry ----|---- work entry ----|
        #         |------------------- hr.leave ---------------|
        #                             ||
        #                             vv
        #     |----* work entry ****|
        #         |************ work entry leave --------------|
        # """
        # if not self:
        #     return

        # # 1. Create a work entry for each leave
        # work_entries_vals_list = []
        # for leave in self:
        #     contracts = leave.employee_id.sudo()._get_contracts(leave.date_from, leave.date_to, states=['open', 'close'])
        #     for contract in contracts:
        #         # Generate only if it has aleady been generated
        #         # if leave.date_to >= contract.date_generated_from and leave.date_from <= contract.date_generated_to:
        #         work_entries_vals_list += contracts._get_work_entries_values(leave.date_from, leave.date_to)
        # print("===========================================================");
        # print("================= logging zzz =================");
        # print("============== work_entries_vals_list description ------->","work_entries_vals_list -> {}".format(work_entries_vals_list));
        # print("================= logging zzz =================");
        # print("===========================================================");
        
        # new_leave_work_entries = self.env['hr.work.entry'].create(work_entries_vals_list)
        # if new_leave_work_entries:
        #     # 2. Fetch overlapping work entries, grouped by employees
        #     start = min(self.mapped('date_from'), default=False)
        #     stop = max(self.mapped('date_to'), default=False)
        #     work_entry_groups = self.env['hr.work.entry'].read_group([
        #         ('date_start', '<', stop),
        #         ('date_stop', '>', start),
        #         ('employee_id', 'in', self.employee_id.ids),
        #     ], ['work_entry_ids:array_agg(id)', 'employee_id'], ['employee_id', 'date_start', 'date_stop'], lazy=False)
        #     work_entries_by_employee = defaultdict(lambda: self.env['hr.work.entry'])
        #     for group in work_entry_groups:
        #         employee_id = group.get('employee_id')[0]
        #         work_entries_by_employee[employee_id] |= self.env['hr.work.entry'].browse(group.get('work_entry_ids'))

        #     # 3. Archive work entries included in leaves
        #     included = self.env['hr.work.entry']
        #     overlappping = self.env['hr.work.entry']
        #     for work_entries in work_entries_by_employee.values():
        #         # Work entries for this employee
        #         new_employee_work_entries = work_entries & new_leave_work_entries
        #         previous_employee_work_entries = work_entries - new_leave_work_entries

        #         # Build intervals from work entries
        #         leave_intervals = new_employee_work_entries._to_intervals()
        #         conflicts_intervals = previous_employee_work_entries._to_intervals()

        #         # Compute intervals completely outside any leave
        #         # Intervals are outside, but associated records are overlapping.
        #         outside_intervals = conflicts_intervals - leave_intervals

        #         overlappping |= self.env['hr.work.entry']._from_intervals(outside_intervals)
        #         included |= previous_employee_work_entries - overlappping
        #     overlappping.write({'leave_id': False})
        #     included.write({'active': False})


    def write(self, vals):
        # if not self:
        #     print("===========================================================");
        #     print("================= logging zzz =================");
        #     print("============== self description ------->","self -> {}".format(self));
        #     print("================= logging zzz =================");
        #     print("===========================================================");
            
        #     a = 1/0
        # print("===========================================================");
        # print("================= logging zzz =================");
        # print("============== self description ------->","self -> {}".format(self));
        # print("================= logging zzz =================");
        # print("===========================================================");
        
       
        if 'state' in vals:
            if vals.get('state') == 'validate':
                if self:
                    if self.holiday_status_id.work_entry_type_id:
                        # todo dont harcode this, use self.env.ref
                        lembur_level = False
                        if self.holiday_status_id.work_entry_type_id.name in ['Lembur']:
                      
                            # todo i think theres cleanier way
                            if self.number_of_hours_display:
                                hour = self.number_of_hours_display
                                if hour <= 1:
                                    lembur_level = 1
                                elif 1 < hour <= 2:
                                    lembur_level = 2
                                elif 2 < hour <= 3:
                                    lembur_level = 3
                                elif 3 < hour <= 4:
                                    lembur_level = 4
                                elif 4 < hour:
                                    lembur_level = 5

                                print("===========================================================");
                                print("================= logging zzz =================");
                                print("============== lembur_level description ------->","lembur_level -> {}".format(lembur_level));
                                print("================= logging zzz =================");
                                print("===========================================================");
                                
                            else:
                                raise UserError("Please fill hours")
                        
                        self.env['hr.work.entry'].create({
                            'state': 'draft',
                            'name': "{} : {}".format(self.holiday_status_id.work_entry_type_id.name,self.employee_id.name),
                            'employee_id': self.employee_id.id,
                            'work_entry_type_id': self.holiday_status_id.work_entry_type_id.id,
                            'date_start': self.date_from,
                            'date_stop': self.date_to,
                            'lembur_level': str(lembur_level) if lembur_level else False
                        })
                    else:
                        raise UserError("You must assign work_entry_type_id for this leave")
            
        res = super().write(vals)
        return res
    # def action_validate(self):
    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== self description ------->","self -> {}".format(self));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
        
    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== self.employee_ids description ------->","self.employee_ids -> {}".format(self.employee_ids));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== self.holiday_status_id description ------->","self.holiday_status_id -> {}".format(self.holiday_status_id));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
        
        
    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== date_from description ------->","date_from -> {}".format(self.date_from));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== date_from description ------->","date_from -> {}".format(self.date_from));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== self.request_date_from description ------->","self.request_date_from -> {}".format(self.request_date_from));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== self.request_date_to description ------->","self.request_date_to -> {}".format(self.request_date_to));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
        
        
    #     self.env['hr.work.entry'].create({
    #         'state': 'draft',
    #         'name': 'Attendance: Reza Mingguan',
    #         'employee_id': 3,
    #         'work_entry_type_id': self.holiday_status_id.work_entry_type_id.id,
    #         'leave_id': False,
    #         'contract_id': 3,
    #         'date_start': self.date_from,
    #         'date_stop': self.date_to,
    #         'duration': 23.99972222222222
    #     })
    #     # ! ini ntar disable ni function
    #     # self.sudo()._cancel_work_entry_conflict()  # delete preexisting conflicting work_entries
    #     super(HrLeave, self).action_validate()
    #     return True