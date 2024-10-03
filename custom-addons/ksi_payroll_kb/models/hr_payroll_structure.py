from odoo import _, api, fields, models

class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'
    
    # ! turn off default
    rule_ids = fields.One2many(
        'hr.salary.rule', 'struct_id',
        default=False)
 
