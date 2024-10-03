# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from pytz import timezone
import pytz
import datetime


class CouponRule(models.Model):
    _inherit = 'coupon.rule'

    custom_rule_date_from = fields.Datetime(string="Start Date", help="Coupon program start date")
    custom_rule_date_to = fields.Datetime(string="End Date", help="Coupon program end date")
    
    @api.onchange('custom_rule_date_from', 'custom_rule_date_to')
    def _onchange_custom_rule_date(self):
        for rec in self:
            if rec.custom_rule_date_from:
                rule_date_from = pytz.UTC.localize(rec.custom_rule_date_from).astimezone(timezone('Asia/Jakarta'))
                rec.rule_date_from = datetime.datetime.strptime(str(rule_date_from.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
            if rec.custom_rule_date_to:
                rule_date_to = pytz.UTC.localize(rec.custom_rule_date_to).astimezone(timezone('Asia/Jakarta'))
                rec.rule_date_to = datetime.datetime.strptime(str(rule_date_to.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')

    @api.constrains('rule_min_quantity')
    def _check_rule_min_quantity(self):
        return True
