from odoo import _, api, fields, models
from datetime import datetime, date, timedelta
import pytz
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    # todo, is it good to put lembur amount in here? not in compute payslip?
    # ! lembur level receive from hr.leave created lembur
    lembur_level = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Lembur Level')
    lembur_amount = fields.Float(store=True,compute='_compute_lembur_amount', string='Lembur Amount')
    
    @api.depends('lembur_level','employee_id','work_entry_type_id')
    def _compute_lembur_amount(self):
        for rec in self:
            if rec.work_entry_type_id:
                # todo, dont harcode this
                if rec.work_entry_type_id.name == "Lembur" and rec.employee_id:
                # if rec.employee_id.contract_id.job_id:
                #     # todo, dont harcode this
                #     position_name = rec.employee_id.contract_id.job_id.name
                #     if position_name in ['Driver','Helper']:
                #         if rec.lembur_level == "1":
                #             rec.lembur_amount = 15000 if position_name == "Driver" else 10000
                #         elif rec.lembur_level == "2":
                #             rec.lembur_amount = 25000 if position_name == "Driver" else 15000
                #         elif rec.lembur_level == "3":
                #             rec.lembur_amount = 35000 if position_name == "Driver" else 20000
                #         elif rec.lembur_level == "4":
                #             rec.lembur_amount = 40000 if position_name == "Driver" else 35000
                #         elif rec.lembur_level == "5":
                #             rec.lembur_amount = 50000
                #         else:
                #             rec.lembur_amount = False
                #     else:
                #         raise UserError("Only Driver or Helper gets lembur amount")
                # ! REFACTORED BY CHATGPT
                    if rec.employee_id.contract_id.job_id:
                        position_name = rec.employee_id.contract_id.job_id.name
                        # todo, dont harcode this
                        if position_name in ['Driver', 'Helper']:
                            lembur_level_amounts = {
                                '1': (15000 if position_name == 'Driver' else 10000),
                                '2': (25000 if position_name == 'Driver' else 15000),
                                '3': (35000 if position_name == 'Driver' else 20000),
                                '4': (40000 if position_name == 'Driver' else 35000),
                                '5': 50000
                            }
                            rec.lembur_amount = lembur_level_amounts.get(rec.lembur_level, False)
                        else:
                            raise UserError("Only Driver or Helper can get lembur amount")

                    else:
                        raise UserError("Please fill the job position of employee : %s"%(rec.employee_id.name))


    def check_daily_absence(self):
        # ! to change contract state if already expired
        self.env.ref('hr_contract.ir_cron_data_contract_update_state').sudo().method_direct_trigger()
        list_contract = self.env['hr.contract.history'].search([('is_under_contract', '=', True)]).mapped('employee_id')
        # ! kyknya harus ada boolean ni employee udah absen blm hari ini
        for employee in list_contract:
            print("===========================================================");
            print("================= logging zzz =================");
            print("============== employee.name description ------->","employee.name -> {}".format(employee.name));
            print("================= logging zzz =================");
            print("===========================================================");
            
            


    def _default_work_entry_type(self):
        default_wet = self.env['hr.work.entry.type'].search([('is_attendance', '=', True)])
        if default_wet:
            return default_wet[0].id
        else:
            return False

    work_entry_type_id = fields.Many2one('hr.work.entry.type', default=_default_work_entry_type)

    schedule_date_start = fields.Datetime('Schedule Date Start', compute="_compute_ksi_contract", store=True)
    schedule_date_stop = fields.Datetime('Schedule Date Stop', compute="_compute_ksi_contract", store=True)
    work_hours = fields.Float('Work Hours')
    is_late = fields.Boolean('Is Late', compute="_compute_ksi_contract", store=True)
    resource_calendar_id = fields.Many2one('resource.calendar', string='Shift', compute="_compute_ksi_contract", store=True)
    late_hours = fields.Float('Late Hours', compute="_compute_ksi_contract", store=True)

    @api.depends('contract_id','date_start','date_stop','work_entry_type_id')
    def _compute_ksi_contract(self):
        for rec in self:
            if rec.work_entry_type_id:
                if rec.work_entry_type_id.is_attendance:
                    if rec.contract_id:
                        # ! cari shift based on tanggal
                        # todo is it safe just to check only based on checkin?
                        # todo check if if nya kalo ada user error
                        # todo pergantian timezonenya masih hardcode
                        if rec.contract_id.shift_schedule:
                            for shift in rec.contract_id.shift_schedule:
                                timezone = pytz.timezone('Asia/Jakarta')

                                # ! this will be always utc, thats why we need to convert it
                                cek = rec.date_start
                                now_local = timezone.fromutc(cek)
                                check_in_date = now_local.date()
                           
                                # ! date and datetime always be problem in odoo
                                if shift.start_date <= check_in_date <= shift.end_date:
                                    shift_rec = shift.hr_shift

                                    rec.resource_calendar_id = shift_rec.id
                                    # ! assign scheduled
                                    # ? compute mending disatuin apa dipisah? secara performa gimana?
                                    # todo what happen if there are more than 1 day, or nothing dayofweek kyk sabtu minggu
                                    day_rec = shift_rec.attendance_ids.filtered(lambda att:  att.dayofweek == str(check_in_date.weekday()))
                                    if day_rec:
                                        day_rec = day_rec[0]
                                        if day_rec.schedule_from and day_rec.schedule_to:
                                            schedule_start = '{0:02.0f}:{1:02.0f}'.format(*divmod(day_rec.schedule_from * 60, 60))
                                            schedule_end = '{0:02.0f}:{1:02.0f}'.format(*divmod(day_rec.schedule_to * 60, 60))
                                            # ! turn in to asia timezone, because default odoo is utc 00
                                            rec.schedule_date_start = '{} {}'.format(check_in_date,schedule_start)
                                            rec.schedule_date_stop = '{} {}'.format(check_in_date,schedule_end)

                                            # rec.schedule_date_start = '2023-03-23 08:00:00'
                                            # rec.schedule_date_stop = '2023-03-23 08:00:00'
                                            
                                            rec.schedule_date_start = rec.schedule_date_start - timedelta(hours=7)
                                            rec.schedule_date_stop = rec.schedule_date_stop - timedelta(hours=7)


                                            # ! is late
                                            if rec.date_start > rec.schedule_date_start:
                                                rec.is_late = True
                                                in_schedule = datetime.strptime(str(rec.schedule_date_start), '%Y-%m-%d %H:%M:%S')
                                                check_in = datetime.strptime(str(rec.date_start), '%Y-%m-%d %H:%M:%S')
                                                delta = check_in - in_schedule
                                                
                                                hours = (delta.total_seconds()) / 3600.0
                                                rec.late_hours = hours
                                            else:
                                                rec.is_late = False
                                        else:
                                            rec.schedule_date_start = False
                                            rec.schedule_date_stop = False
                                    else:
                                        rec.schedule_date_start = False
                                        rec.schedule_date_stop = False
                                        # raise UserError(_("Theres no dayofweek shift on {}".format(check_in_date.strftime('%A'))))

                                    break
                else:
                    rec.schedule_date_start = False
                    rec.schedule_date_stop = False
                         

                            # else:
                            #     rec.schedule_date_start = False
                            #     rec.schedule_date_stop = False

                        # todo assign is_late if telat
           
            
            # ! cek punya kontrak sesuai tanggal check in?
            # ! set shift based on tanggal
            # ! set schedule based on tanggal

            else:
                rec.resource_calendar_id = False
                rec.schedule_date_start = False
                rec.schedule_date_stop = False

    # @api.model
    # def write(self, vals):
    #     print("===========================================================");
    #     print("================= logging zzz =================");
    #     print("============== vals description ------->","vals -> {}".format(vals));
    #     print("================= logging zzz =================");
    #     print("===========================================================");
    #     if 'schedule_date_start' in vals:
    #         a = 1/0
    @api.model_create_multi
    def create(self, vals):
        print("===========================================================");
        print("================= logging zzz =================");
        print("============== vals description ------->","vals -> {}".format(vals));
        print("================= logging zzz =================");
        print("===========================================================");
        
        res = super(HrWorkEntry, self).create(vals)
        
        return res


class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    is_attendance = fields.Boolean('Is Attendance')
    is_absence = fields.Boolean('Is Absence')
