from odoo import _, api, fields, models
from pytz import timezone
import pytz
import datetime


class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    @api.onchange('custom_rule_date_from', 'custom_rule_date_to')
    def _onchange_custom_rule_date(self):
        for rec in self:
            if rec.custom_rule_date_from:
                rule_date_from = pytz.UTC.localize(rec.custom_rule_date_from).astimezone(timezone('Asia/Jakarta'))
                rec.rule_date_from = datetime.datetime.strptime(str(rule_date_from.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
            if rec.custom_rule_date_to:
                rule_date_to = pytz.UTC.localize(rec.custom_rule_date_to).astimezone(timezone('Asia/Jakarta'))
                rec.rule_date_to = datetime.datetime.strptime(str(rule_date_to.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')