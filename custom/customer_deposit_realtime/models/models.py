# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class customer_deposit_realtime(models.Model):
#     _name = 'customer_deposit_realtime.customer_deposit_realtime'
#     _description = 'customer_deposit_realtime.customer_deposit_realtime'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
