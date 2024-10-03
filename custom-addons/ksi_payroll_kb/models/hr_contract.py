from odoo import _, api, fields, models
import pytz
from datetime import datetime
from odoo.exceptions import UserError
class HrContract(models.Model):
    _inherit = 'hr.contract'

    # ! formula perhitungan gaji 

    def calc_lembur(self,payslip):
        # ! convert to tz, and utc
        dt_from = datetime.combine(payslip.date_from, datetime.min.time())
        dt_to = datetime.combine(payslip.date_to, datetime.min.time())

        # ! bcs mingguan date start must accumulate 1 month
        dt_from = dt_from.replace(day=1)

        # utc_tz = pytz.UTC
        # dt_utc = utc_tz.localize(dt)

        # jakarta_tz = pytz.timezone('Asia/Jakarta')
        # dt_jakarta = dt_utc.astimezone(jakarta_tz)

        jakarta_tz = pytz.timezone('Asia/Jakarta')
        dt_jakarta_from = jakarta_tz.localize(dt_from)
        dt_jakarta_to = jakarta_tz.localize(dt_to)


        utc_tz = pytz.UTC
        dt_utc_from = dt_jakarta_from.astimezone(utc_tz)
        dt_utc_to = dt_jakarta_to.astimezone(utc_tz)

        # todo dont harcode the we type
        lembur_rec = self.env['hr.work.entry'].search([
            ('employee_id', '=', payslip.employee_id),
            ('work_entry_type_id.name', '=', ('LEMBUR','Lembur')),
            ('date_start', '>=', dt_utc_from),
            ('date_start', '<=', dt_utc_to)
        ])

        amount_lembur = 0
        for lembur in lembur_rec:
            amount_lembur += lembur.lembur_amount
        
        return amount_lembur

    def check_minggu(self, payslip):
        # ! return gaji ke 1/2
        middle_date = [14,15,16]
        end_date = [28,29,30,31]

        if int(payslip.date_to.strftime("%d")) in middle_date:
            return 1
        elif int(payslip.date_to.strftime("%d")) in end_date:
            return 2
        
        
        else:
            raise UserError(_("You cannot compute weekly sheet with this date"))


    # def calc_gaji_mingguan(self, payslip):
    #     middle_date = [14,15,16]
    #     end_date = [28,29,30,31]

    #     if int(payslip.date_to.strftime("%d")) in middle_date:
    #         return round(self.gaji_harian * 13)
    #     elif int(payslip.date_to.strftime("%d")) in end_date:
    #         return round(self.gaji_harian * 10)
        
        
    #     return 555

    def calc_work_entries(self):
        return 0

    def calc_long_shift(self,payslip):
        # ! convert to tz, and utc
        dt_from = datetime.combine(payslip.date_from, datetime.min.time())
        dt_to = datetime.combine(payslip.date_to, datetime.min.time())

        # ! bcs mingguan date start must accumulate 1 month
        dt_from = dt_from.replace(day=1)

        # utc_tz = pytz.UTC
        # dt_utc = utc_tz.localize(dt)

        # jakarta_tz = pytz.timezone('Asia/Jakarta')
        # dt_jakarta = dt_utc.astimezone(jakarta_tz)

        jakarta_tz = pytz.timezone('Asia/Jakarta')
        dt_jakarta_from = jakarta_tz.localize(dt_from)
        dt_jakarta_to = jakarta_tz.localize(dt_to)


        utc_tz = pytz.UTC
        dt_utc_from = dt_jakarta_from.astimezone(utc_tz)
        dt_utc_to = dt_jakarta_to.astimezone(utc_tz)

        # todo dont harcode the we type
        longshift_rec = self.env['hr.work.entry'].search([
            ('employee_id', '=', payslip.employee_id),
            ('work_entry_type_id.name', 'in', ('LONGSHIFT','Longshift')),
            ('date_start', '>=', dt_utc_from),
            ('date_start', '<=', dt_utc_to)
        ])
        amount_longshift = 0
        for longshift in longshift_rec:
            amount_longshift += 50000

        return amount_longshift