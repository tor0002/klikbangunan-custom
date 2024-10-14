# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_minmax_price(models.Model):
#     _name = 'custom_minmax_price.custom_minmax_price'
#     _description = 'custom_minmax_price.custom_minmax_price'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
