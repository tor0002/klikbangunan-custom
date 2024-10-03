from odoo import models, fields, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    custom_approval = fields.Boolean(string='Custom Approval')
    approval_type = fields.Selection([
        ('user', 'By User'),
        ('group', 'By Group')
    ], string='Approval Type', default='user')
    purchase_approval_line = fields.One2many('purchase.approval', 'company_id', string='Purchase Approval')

    @api.onchange('approval_type')
    def _onchange_approval_type(self):
        if len(self.purchase_approval_line) >= 1:
            raise ValidationError(("You can not change Approval Type when Purchase Approval Line it's not empty !"))


class PurchaseApproval(models.Model):
    _name = 'purchase.approval'
    _description = 'Purchase Approval'

    name = fields.Char(string='Reference')
    sequence = fields.Integer(string='No', readonly=True, store=True, compute="_sequence_ref")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    company_id = fields.Many2one('res.company', string='Company')
    minimal_amount = fields.Monetary(string="Minimal Amount", currency_field="currency_id", required=True)
    user_ids = fields.Many2many('res.users', string='User')
    group_ids = fields.Many2many('res.groups', string='Groups')

    @api.model
    def create(self, vals):
        approval = self.env['purchase.approval'].search([('company_id.name', '=', self.env.user.company_id.name)], limit=1, order='sequence desc')
        if approval:
            if vals['minimal_amount'] < approval.minimal_amount:
                raise ValidationError(("Minimal amount must be greater than previos approval !"))
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.approval')
        return super(PurchaseApproval, self).create(vals)

    @api.model
    def write(self, vals):
        res = super(PurchaseApproval, self).write(vals)
        approval = self.env['purchase.approval'].search([('company_id.name', '=', self.env.user.company_id.name), ('sequence', '<', self.sequence)], limit=1, order='sequence desc')
        first_approval = self.env['purchase.approval'].search([('company_id.name', '=', self.env.user.company_id.name), ('sequence', '>', self.sequence)], limit=1, order='sequence asc')
        if first_approval and 'minimal_amount' in vals:
            if vals['minimal_amount'] > first_approval.minimal_amount:
                raise ValidationError(("For the first approval, minimal amount must be lower than next approval !"))

        if approval and 'minimal_amount' in vals:
            if vals['minimal_amount'] < approval.minimal_amount:
                raise ValidationError(("Minimal amount must be greater than previos approval !"))
        return res

    @api.depends('company_id.purchase_approval_line', 'company_id.purchase_approval_line.minimal_amount')
    def _sequence_ref(self):
        for line in self:
            no = 0
            for l in line.company_id.purchase_approval_line:
                no += 1
                l.sequence = no
