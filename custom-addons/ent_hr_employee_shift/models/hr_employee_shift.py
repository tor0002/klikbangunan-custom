# -*- coding: utf-8 -*-
######################################################################################
#
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class HrEmployeeInherited(models.Model):
    _inherit = 'hr.employee'

    resource_calendar_ids = fields.\
        Many2one('resource.calendar', 'Working Hours')


class HrEmployeeShift(models.Model):
    _inherit = 'resource.calendar'

    def _get_default_attendance_ids(self):
        return [
            (0, 0, {'name': _('Monday Morning'), 'dayofweek': '0',
                    'hour_from': 8, 'hour_to': 12}),
            (0, 0, {'name': _('Tuesday Morning'), 'dayofweek': '1',
                    'hour_from': 8, 'hour_to': 12}),
            (0, 0, {'name': _('Wednesday Morning'), 'dayofweek': '2',
                    'hour_from': 8, 'hour_to': 12}),
            (0, 0, {'name': _('Thursday Morning'), 'dayofweek': '3',
                    'hour_from': 8, 'hour_to': 12}),
            (0, 0, {'name': _('Friday Morning'), 'dayofweek': '4',
                    'hour_from': 8, 'hour_to': 12}),
        ]

    color = fields.Integer(string='Color Index', help="Color")
    hr_department = fields.Many2one('hr.department', string="Department", help="Department")
    sequence = fields.Integer(string="Sequence", required=True, default=1,
                              help="Sequence")
    attendance_ids = fields.One2many(
        'resource.calendar.attendance', 'calendar_id', 'Workingssss Time',
        copy=True, default=_get_default_attendance_ids)

    @api.constrains('sequence')
    def validate_seq(self):
        if self.id:
            record = self.env['resource.calendar']\
                .search([('sequence', '=', self.sequence),
                         ('company_id', '=', self.company_id.id)])
            if len(record) > 1:
                raise ValidationError("One record with same sequence is "
                                      "already active. You can't activate "
                                      "more than one record  at a time")

class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    schedule_from = fields.Float(string='Schedule from', required=True, index=True,
        help="Start and End time of working.\n"
             "A specific value of 24:00 is interpreted as 23:59:59.999999.")
    schedule_to = fields.Float(string='Schedule to', required=True)    
