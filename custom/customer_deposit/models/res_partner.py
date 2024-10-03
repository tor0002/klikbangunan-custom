from odoo import api, fields, models, tools, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    deposit_amount = fields.Float('Customer Deposit', compute='_compute_customer_deposit')
    move_line_ids = fields.One2many('account.move.line', 'partner_id', string='Account Move')
    total_unpaid_invoice = fields.Float('Total Unpaid Invoice', compute='_compute_unpaid_invoice')
    
    #Technical Porpose
    amount_deposit = fields.Float('Deposit')

    def action_invoice_register_payment(self):
        for partner in self:            
            return self.env['account.payment']\
                .with_context(
                    active_ids=partner.ids,
                    active_model='res.partner',
                    active_id=partner.id,
                    default_communication='Deposit %s' % partner.name,
                    default_partner_id=partner.id,
                    default_partner_type='customer',
                    default_payment_type='inbound')\
                .action_register_payment()

    def _set_update_deposit(self):
        for record in self:
            if record.deposit_amount != record.amount_deposit:
                record.update({'amount_deposit': record.deposit_amount})

    @api.depends('move_line_ids')
    def _compute_customer_deposit(self):
        lines = self.env['account.move.line'].sudo()
        for partner in self:
            domain = [('account_internal_type', 'in', ('receivable','payable')), '|', ('move_id.state', '=', 'posted'), '&', ('move_id.state', '=', 'draft'), ('journal_id.post_at', '=', 'bank_rec'), ('partner_id', '=', partner.id), ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0),('amount_residual_currency', '!=', 0.0)]
            total_lines = lines.search(domain)
            net = sum(line.credit for line in total_lines) - sum(line.debit for line in total_lines)
            partner.write({'deposit_amount': net if net >= 0.0 else 0.0})

    @api.depends('move_line_ids')
    def _compute_unpaid_invoice(self):
        moves = self.env['account.move'].sudo()
        for partner in self:
            domain = [
                ('company_id', '=', self.env.company.id),
                ('commercial_partner_id', '=', partner.id),
                ('state', '=', 'posted'),
                ('invoice_payment_state', '!=', 'paid'),
                ('type', 'in', self.env['account.move'].get_sale_types())
            ]
            total_moves = moves.search(domain)
            partner.update({'total_unpaid_invoice': sum(move.amount_residual for move in total_moves)})                