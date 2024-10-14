# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_ds_validation(models.Model):
#     _name = 'custom_ds_validation.custom_ds_validation'
#     _description = 'custom_ds_validation.custom_ds_validation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
