# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    documents_spreadsheet_folder_id = fields.Many2one(required=False)

    def action_generate(self):
        self.env['ksi.report.kb.sale.transaction'].generate()
        
    def action_print(self):
        return self.env['ksi.report.kb.sale.transaction'].action_print()
        
    def do_export(self):
        return self.env['ksi.report.kb.sale.transaction'].do_export()
    
    def action_clear(self):
        self.env['ksi.report.kb.sale.transaction'].clear_data()
        
# class ResCompany(models.Model):
#     _inherit = 'res.company'    
