
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class KsiReportKbSaleTransactionWizard(models.TransientModel):
    _name = 'ksi.report.kb.sale.transaction.wizard'
    _description = 'KSI Report KB - Sale Transaction Wizard (original)'

    warning_message = fields.Text('Warning Message', default="Use this wizard to Print Sale Transaction data")
    
    def action_generate(self):
        # action = {
        #     'name'      : 'ksi_report_kb_sale_transaction_list',
        #     'type'      : 'ir.actions.act_window',
        #     'res_model' : 'ksi.report.kb.sale.transaction',
        #     'view_mode' : 'tree',
        #     'view_type' : 'tree',
        #     'target'    : 'current'
        #     }
        # return action
    
        ref = self.env.ref('ksi_report_kb.ksi_report_kb_sale_transaction_action')
        model = 'ksi.report.kb.sale.transaction'
        # return ref #.report_action(self)
    
        return {
            'name': _('test'),
            'view_type': 'form',
            'view_mode': 'tree',
            'view_id': ref.id,
            'res_model': model,
            # 'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


    def action_print(self):
        return self.env.ref('ksi_report_kb.report_kb_sale_transaction').report_action(self)
    
    def do_export(self):
        return self.env.ref('ksi_report_kb.report_kb_sale_transaction').report_action(self.env['ksi.report.kb.sale.transaction'])