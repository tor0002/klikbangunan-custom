# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ksi_report_kb(models.Model):
#     _name = 'ksi_report_kb.ksi_report_kb'
#     _description = 'ksi_report_kb.ksi_report_kb'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
