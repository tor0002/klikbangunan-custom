# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ksi_inventory_kb(models.Model):
#     _name = 'ksi_inventory_kb.ksi_inventory_kb'
#     _description = 'ksi_inventory_kb.ksi_inventory_kb'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100