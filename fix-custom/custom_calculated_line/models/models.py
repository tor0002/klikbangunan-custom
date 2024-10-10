# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_calculated_line(models.Model):
#     _name = 'custom_calculated_line.custom_calculated_line'
#     _description = 'custom_calculated_line.custom_calculated_line'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
