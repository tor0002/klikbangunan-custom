from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class HrAbsentWizard(models.TransientModel):
    _name = 'hr.absent.wizard'
    _description = 'Hr Absent Wizard'
    
    employee_ids = fields.Many2many('hr.employee', string='Employee')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    def generate_absent(self):
        print("===========================================================");
        print("================= logging zzz =================");
        print("============== date_from.to_datetime() description ------->","date_from.to_datetime() -> {}".format(self.date_from.to_datetime()));
        print("================= logging zzz =================");
        print("===========================================================");
        
        
        min_date = datetime.combine(self.date_from, datetime.min.time())
        max_date = datetime.combine(self.date_to, datetime.min.time())

        tes = self.env['hr.work.entry'].sudo().search([])
        print("===========================================================");
        print("================= logging zzz =================");
        print("============== tes.date_start description ------->","tes.date_start -> {}".format(tes.date_start));
        print("================= logging zzz =================");
        print("===========================================================");
        
     
        
        for date in (min_date + timedelta(n) for n in range((max_date - min_date).days + 1)):
            print("===========================================================");
            print("================= logging zzz =================");
            print("============== date description ------->","date -> {}".format(date));
            print("================= logging zzz =================");
            print("===========================================================");
            
        self.env['hr.work.entry'].create([
            {
                'name' : "eas",
                'work_entry_type_id' : 1,
                'employee_id' : 3,
                'date_start': '2023-04-02 01:00:00',
                'date_stop' : '2023-04-02 15:00:00'
            }
        ])

        raise UserError("debug")

        # ! return to gant
        action = self.env.ref('hr_work_entry.hr_work_entry_action').read()[0]
        return action   