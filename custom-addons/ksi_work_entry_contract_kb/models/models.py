# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ksi_work_entry_contract_kb(models.Model):
#     _name = 'ksi_work_entry_contract_kb.ksi_work_entry_contract_kb'
#     _description = 'ksi_work_entry_contract_kb.ksi_work_entry_contract_kb'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
