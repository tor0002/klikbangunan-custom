from odoo import models, fields, api
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_refused = fields.Boolean(string='Is Refused', copy=False)
    is_approval = fields.Boolean(string='Is Approval', compute='_user_can_approve')
    custom_approval = fields.Boolean(string='Custom Approval', related="company_id.custom_approval", store=True)
    approval_id = fields.Many2one('purchase.approval', string='Purchase Approval', copy=False)
    last_approval_id = fields.Many2one('res.users', string='Last Approved By', copy=False, track_visibility='onchange', readonly=True, store=True)
    last_approval_date = fields.Datetime(string='Date of Last Approval', copy=False, readonly=True, store=True)
    refused_id = fields.Many2one('res.users', string='Refused By', track_visibility='onchange', copy=False, readonly=True, store=True)
    refused_date = fields.Datetime(string='Refused Date', copy=False, store=True, readonly=True)
    refused_reason = fields.Text(string='Reason', track_visibility='onchange', copy=False, readonly=True, store=True)

    def button_request(self):
        if self.custom_approval:
            approval = self.env['purchase.approval'].search([('company_id', '=', self.company_id.id), ('minimal_amount', '<=', self.amount_total)], limit=1)
            if approval:
                self.state = 'to approve'
                self.approval_id = approval.id
            else:
                self.button_confirm()

    @api.depends('approval_id')
    def _user_can_approve(self):
        for s in self:
            if s.approval_id:
                for r in s.approval_id.user_ids:
                    if s.approval_id.user_ids and not s.is_approval:
                        s.is_approval = s._uid in r.ids

                for i in s.approval_id.group_ids:
                    if s.approval_id.group_ids and not s.is_approval:
                        s.is_approval = s._uid in i.users.ids
            else:
                s.is_approval = False

    def button_custom_approval(self):
        self.write({'last_approval_id': self.env.user.id})
        self.write({'last_approval_date': datetime.now()})
        approval = self.env['purchase.approval'].search([('company_id', '=', self.company_id.id), ('minimal_amount', '<=', self.amount_total), ('sequence', '>', self.approval_id.sequence)], limit=1)
        if approval:
            self.approval_id = approval.id
        else:
            self.button_approve()

    def refused_purchase_order(self):
        view_id = self.env.ref('ab_dynamic_purchase_approval.refused_wizard_form_view')

        return {
            'name': ('Refused Order'),
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'refused.order',
            'view_id': view_id.id,
            'type': 'ir.actions.act_window',
        }
