import json
from odoo import _,models,api,fields
# from num2words import num2words
# from odoo.tools.misc import formatLang, format_date, get_lang
# from collections import defaultdict
# from lxml import etree
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    discount_amount = fields.Monetary('Discount Amount', compute="_get_discount_amount")
    amount_after_disc = fields.Monetary('Amount after Discount', compute='_compute_after_disc', store=True)

    partner_id_domain = fields.Char(
        compute="_compute_partner_id_domain",
        readonly=True,
        store=False,
    )
    
    @api.depends('journal_id')
    def _compute_partner_id_domain(self):
        for rec in self:
            if (rec.journal_id.type == 'sale'):
                print("INI INVOICE!")
                rec.partner_id_domain = json.dumps(
                    [('customer_rank', '>', 0)]
                )
            elif (rec.journal_id.type == 'purchase'):
                print("INI VENDOR BILL!")
                rec.partner_id_domain = json.dumps(
                    [('supplier_rank', '>', 0)]
                )
            else:
                print("INI GAK JELAS!")
                rec.partner_id_domain = json.dumps(
                    []
                )
                
    is_new_purchase = fields.Boolean(compute='_compute_is_new_purchase', string='Is New Purchase?', store=True)
    
    @api.depends('invoice_origin')
    def _compute_is_new_purchase(self):
        for rec in self:
            rec.is_new_purchase = True if rec.journal_id.type == 'purchase' and not rec.invoice_origin else False
            
    @api.constrains('l10n_id_kode_transaksi', 'line_ids')
    def _constraint_kode_ppn(self):
        ppn_tag = self.env.ref('l10n_id.ppn_tag')
        for move in self.filtered(lambda m: m.l10n_id_kode_transaksi != '08'):
            if any(ppn_tag.id in line.tax_tag_ids.ids for line in move.line_ids if line.exclude_from_invoice_tab is False and not line.display_type) \
                    and any(ppn_tag.id not in line.tax_tag_ids.ids for line in move.line_ids if line.exclude_from_invoice_tab is False and not line.display_type):
                msg = _('Cannot mix VAT subject and Non-VAT subject items in the same invoice with this transaction code.')
                print(msg)
                # raise UserError(msg)
        for move in self.filtered(lambda m: m.l10n_id_kode_transaksi == '08'):
            if any(ppn_tag.id in line.tax_tag_ids.ids for line in move.line_ids if line.exclude_from_invoice_tab is False and not line.display_type):
                msg = 'Transaction with code 08 is only for Non-VAT subject items!'
                print(msg)
                # raise UserError(msg)
    
    @api.depends('amount_untaxed')
    def _compute_after_disc(self):
        for rec in self : 
            amount_after_disc = 0
            # if rec.global_discount:
            #     discount = rec.amount_untaxed * rec.global_discount / 100.0
            #     amount_after_disc = rec.amount_untaxed - discount
            # else:
            #     amount_after_disc = rec.amount_untaxed
            rec.amount_after_disc = rec.amount_untaxed
            rec.amount_after_disc = amount_after_disc
            # rec.amount_total = rec.amount_after_disc + rec.amount_tax

#    #2
#     @api.onchange("invoice_line_ids")
#     def _onchange_invoice_line_ids(self):
#         others_lines = self.line_ids.filtered(
#             lambda line: line.exclude_from_invoice_tab
#         )
#         if others_lines:
#             others_lines[0].recompute_tax_line = True
#         res = super()._onchange_invoice_line_ids()
#         return res

#     #1
#     @api.onchange("global_discount")
#     def _onchange_global_discount(self):
#         """Trigger global discount field to recompute all"""
#         return self._onchange_invoice_line_ids()

    @api.depends('invoice_line_ids.sub_total_disc')
    def _get_discount_amount(self):
        for rec in self:
            rec.discount_amount = sum(rec.invoice_line_ids.mapped('sub_total_disc'))

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id',
        'line_ids.sub_total_disc')
    def _compute_amount(self):
        for move in self:
            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue

            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = set()

            for line in move.line_ids:
                if line.currency_id and line in move._get_lines_onchange_currency():
                    currencies.add(line.currency_id)

                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed) - move.discount_amount
            move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = sign * (total_currency if len(currencies) == 1 else total) - move.discount_amount
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            
            move.amount_untaxed_signed = -total_untaxed - move.discount_amount
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = abs(total) - move.discount_amount if move.move_type == 'entry' else -total - move.discount_amount
            move.amount_residual_signed = total_residual

            currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id

            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move.is_invoice(include_receipts=True) and move.state == 'posted':

                if currency.is_zero(move.amount_residual):
                    reconciled_payments = move._get_reconciled_payments()
                    if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search([('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state

    def _recompute_payment_terms_lines(self):
        ''' Compute the dynamic payment term lines of the journal entry.'''
        self.ensure_one()
        self = self.with_company(self.company_id)
        in_draft_mode = self != self._origin
        today = fields.Date.context_today(self)
        self = self.with_company(self.journal_id.company_id)

        def _get_payment_terms_computation_date(self):
            ''' Get the date from invoice that will be used to compute the payment terms.
            :param self:    The current account.move record.
            :return:        A datetime.date object.
            '''
            if self.invoice_payment_term_id:
                return self.invoice_date or today
            else:
                return self.invoice_date_due or self.invoice_date or today

        def _get_payment_terms_account(self, payment_terms_lines):
            ''' Get the account from invoice that will be set as receivable / payable account.
            :param self:                    The current account.move record.
            :param payment_terms_lines:     The current payment terms lines.
            :return:                        An account.account record.
            '''
            if payment_terms_lines:
                # Retrieve account from previous payment terms lines in order to allow the user to set a custom one.
                return payment_terms_lines[0].account_id
            elif self.partner_id:
                # Retrieve account from partner.
                if self.is_sale_document(include_receipts=True):
                    return self.partner_id.property_account_receivable_id
                else:
                    return self.partner_id.property_account_payable_id
            else:
                # Search new account.
                domain = [
                    ('company_id', '=', self.company_id.id),
                    ('internal_type', '=', 'receivable' if self.move_type in ('out_invoice', 'out_refund', 'out_receipt') else 'payable'),
                ]
                return self.env['account.account'].search(domain, limit=1)

        def _compute_payment_terms(self, date, total_balance, total_amount_currency):
            ''' Compute the payment terms.
            :param self:                    The current account.move record.
            :param date:                    The date computed by '_get_payment_terms_computation_date'.
            :param total_balance:           The invoice's total in company's currency.
            :param total_amount_currency:   The invoice's total in invoice's currency.
            :return:                        A list <to_pay_company_currency, to_pay_invoice_currency, due_date>.
            '''
            if self.invoice_payment_term_id:
                to_compute = self.invoice_payment_term_id.compute(total_balance, date_ref=date, currency=self.company_id.currency_id)
                if self.currency_id == self.company_id.currency_id:
                    # Single-currency.
                    return [(b[0], b[1], b[1]) for b in to_compute]
                else:
                    # Multi-currencies.
                    to_compute_currency = self.invoice_payment_term_id.compute(total_amount_currency, date_ref=date, currency=self.currency_id)
                    return [(b[0], b[1], ac[1]) for b, ac in zip(to_compute, to_compute_currency)]
            else:
                return [(fields.Date.to_string(date), total_balance, total_amount_currency)]

        def _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute, others_lines):
            ''' Process the result of the '_compute_payment_terms' method and creates/updates corresponding invoice lines.
            :param self:                    The current account.move record.
            :param existing_terms_lines:    The current payment terms lines.
            :param account:                 The account.account record returned by '_get_payment_terms_account'.
            :param to_compute:              The list returned by '_compute_payment_terms'.
            '''
            # As we try to update existing lines, sort them by due date.
            existing_terms_lines = existing_terms_lines.sorted(lambda line: line.date_maturity or today)
            existing_terms_lines_index = 0

            analytic_tag_list = []
            for rec in others_lines:
                for res in rec.analytic_tag_ids:
                    analytic_tag_list.append(res.id)

            # Recompute amls: update existing line or create new one for each payment term.
            new_terms_lines = self.env['account.move.line']
            discount_amount = float(round(sum(others_lines.mapped('sub_total_disc'))))
            print("payterm discount_amount", discount_amount)
            discount_amount_convert = self.currency_id._convert(discount_amount, self.company_id.currency_id, self.company_id, self.invoice_date or fields.Date.context_today(self))
            print("payterm discount_amount_convert", discount_amount_convert)
            for date_maturity, balance, amount_currency in to_compute:
                print('ACCOUNT ID PAY TERM', account.name, balance, amount_currency, discount_amount_convert)
                if self.journal_id.company_id.currency_id.is_zero(balance) and len(to_compute) > 1:
                    print("MASUK: self.journal_id.company_id.currency_id.is_zero(balance) and len(to_compute) > 1")
                    continue

                if existing_terms_lines_index < len(existing_terms_lines):
                    # Update existing line.
                    candidate = existing_terms_lines[existing_terms_lines_index]
                    existing_terms_lines_index += 1
                    candidate.update({
                        'date_maturity': date_maturity,
                        'debit': -(balance + discount_amount_convert) if balance < 0.0 else 0.0,
                        'credit': balance - discount_amount_convert if balance > 0.0 else 0.0,
                        'amount_currency': -(amount_currency - discount_amount) if balance > 0.0 else -(amount_currency + discount_amount),
                        'analytic_tag_ids': [(6,0,list(set(analytic_tag_list)))]
                    })
                else:
                    # Create new line.
                    create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
                    candidate = create_method({
                        'name': self.payment_reference or '',
                        'debit': -(balance + discount_amount_convert) if balance < 0.0 else 0.0,
                        'credit': balance - discount_amount_convert if balance > 0.0 else 0.0,
                        'quantity': 1.0,
                        'amount_currency': -(amount_currency - discount_amount) if balance > 0.0 else -(amount_currency + discount_amount),
                        'date_maturity': date_maturity,
                        'move_id': self.id,
                        'currency_id': self.currency_id.id,
                        'account_id': account.id,
                        'partner_id': self.commercial_partner_id.id,
                        'exclude_from_invoice_tab': True,
                        'analytic_tag_ids': [(6,0,list(set(analytic_tag_list)))]
                    })
                
                print('payterm debit', candidate['debit'])
                print('payterm credit', candidate['credit'])
                print('payterm amount_currency', candidate['amount_currency'])
                print("payterm ROUND(debit - credit - amount_currency, 2) = 0 <> ", round(candidate['debit'] - candidate['credit'] - candidate['amount_currency'], 2))
            
                new_terms_lines += candidate
                if in_draft_mode:
                    candidate.update(candidate._get_fields_onchange_balance(force_computation=True))
            return new_terms_lines

        def _compute_discount_lines(self, others_lines):

            journal_type = self.journal_id.type
            print("JOURNAL TYPE", self.journal_id.type)

            discount_lines = self.env['account.move.line']
            discount_account_id = self.company_id.sales_coa_discount_id if journal_type=='sale' else self.company_id.purchases_coa_discount_id
            analytic_tag_list = []
            for rec in others_lines:
                for res in rec.analytic_tag_ids:
                    analytic_tag_list.append(res.id)
            create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
            discount_amount = float(round(sum(others_lines.mapped('sub_total_disc'))))
            print("discount discount_amount", discount_amount)
            discount_amount_convert = self.currency_id._convert(discount_amount, self.company_id.currency_id, self.company_id, self.invoice_date or fields.Date.context_today(self))
            
            if self.line_ids.filtered(lambda x: x.account_id.id == discount_account_id.id): #existing line discount
                print('YES discount line detected', discount_amount_convert)
                discount = self.line_ids.filtered(lambda x: x.account_id.id == discount_account_id.id)
                discount.update({
                    'debit' : discount_amount_convert if journal_type=='sale' else 0,
                    'credit' : discount_amount_convert if journal_type=='purchase' else 0,
                    'quantity': 1.0,
                    'amount_currency': discount_amount if journal_type=='sale' else -discount_amount,
                    'analytic_tag_ids': [(6,0,list(set(analytic_tag_list)))]
                })
            else:
                print('NO discount line detected', discount_amount_convert)
                discount = create_method({
                    'name': 'Discount',
                    'debit' : discount_amount_convert if journal_type=='sale' else 0,
                    'credit' : discount_amount_convert if journal_type=='purchase' else 0,
                    'quantity': 1.0,
                    'amount_currency': discount_amount if journal_type=='sale' else -discount_amount,
                    # 'date_maturity': date_maturity,
                    'move_id': self.id,
                    'currency_id': self.currency_id.id,
                    'account_id': discount_account_id.id,
                    'partner_id': self.commercial_partner_id.id,
                    'exclude_from_invoice_tab': True,
                    'analytic_tag_ids': [(6,0,list(set(analytic_tag_list)))]
                })
            
            print('discount debit', discount['debit'])
            print('discount credit', discount['credit'])
            print('discount amount_currency', discount['amount_currency'])            
            print("discount ROUND(debit - credit - amount_currency, 2) = 0 <> ", round(discount['debit'] - discount['credit'] - discount['amount_currency'], 2))
            
            discount_lines += discount
            return discount_lines

        existing_terms_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
        discount_account_id = self.company_id.sales_coa_discount_id if self.journal_id.type=='sale' else self.company_id.purchases_coa_discount_id
        others_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable') and line.account_id.id != discount_account_id.id)
        company_currency_id = (self.company_id or self.env.company).currency_id
        total_balance = sum(others_lines.mapped(lambda l: company_currency_id.round(l.balance)))
        total_amount_currency = sum(others_lines.mapped('amount_currency'))

        print('TOTAL BALANCE', total_balance)
        print('TOTAL Amount Currency', total_amount_currency)

        if not others_lines:
            self.line_ids -= existing_terms_lines
            return

        discount_lines = _compute_discount_lines(self, others_lines)
        computation_date = _get_payment_terms_computation_date(self)
        account = _get_payment_terms_account(self, existing_terms_lines)
        to_compute = _compute_payment_terms(self, computation_date, total_balance, total_amount_currency)
        new_terms_lines = _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute, others_lines)

        # Remove old terms lines that are no longer needed.
        self.line_ids -= existing_terms_lines - new_terms_lines - discount_lines

        if new_terms_lines:
            self.payment_reference = new_terms_lines[-1].name or ''
            self.invoice_date_due = new_terms_lines[-1].date_maturity

    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        ''' Compute the dynamic tax lines of the journal entry.

        :param lines_map: The line_ids dispatched by type containing:
            * base_lines: The lines having a tax_ids set.
            * tax_lines: The lines having a tax_line_id set.
            * terms_lines: The lines generated by the payment terms of the invoice.
            * rounding_lines: The cash rounding lines of the invoice.
        '''
        self.ensure_one()
        in_draft_mode = self != self._origin

        def _serialize_tax_grouping_key(grouping_dict):
            ''' Serialize the dictionary values to be used in the taxes_map.
            :param grouping_dict: The values returned by '_get_tax_grouping_key_from_tax_line' or '_get_tax_grouping_key_from_base_line'.
            :return: A string representing the values.
            '''
            return '-'.join(str(v) for v in grouping_dict.values())

        def _compute_base_line_taxes(base_line):
            ''' Compute taxes amounts both in company currency / foreign currency as the ratio between
            amount_currency & balance could not be the same as the expected currency rate.
            The 'amount_currency' value will be set on compute_all(...)['taxes'] in multi-currency.
            :param base_line:   The account.move.line owning the taxes.
            :return:            The result of the compute_all method.
            '''
            move = base_line.move_id

            if move.is_invoice(include_receipts=True):
                handle_price_include = True
                sign = -1 if move.is_inbound() else 1
                quantity = base_line.quantity
                is_refund = move.move_type in ('out_refund', 'in_refund')
                price_unit_wo_discount = sign * (base_line.price_unit - (base_line.sub_total_disc / base_line.quantity)) if base_line.sub_total_disc else sign * base_line.price_unit
            else:
                handle_price_include = False
                quantity = 1.0
                tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
                is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)
                price_unit_wo_discount = base_line.balance

            print("********** price_unit_wo_discount **********", price_unit_wo_discount)
            
            balance_taxes_res = base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
                price_unit_wo_discount,
                currency=base_line.currency_id,
                quantity=quantity,
                product=base_line.product_id,
                partner=base_line.partner_id,
                is_refund=is_refund,
                handle_price_include=handle_price_include,
            )

            if move.move_type == 'entry':
                repartition_field = is_refund and 'refund_repartition_line_ids' or 'invoice_repartition_line_ids'
                repartition_tags = base_line.tax_ids.flatten_taxes_hierarchy().mapped(repartition_field).filtered(lambda x: x.repartition_type == 'base').tag_ids
                tags_need_inversion = (tax_type == 'sale' and not is_refund) or (tax_type == 'purchase' and is_refund)
                if tags_need_inversion:
                    balance_taxes_res['base_tags'] = base_line._revert_signed_tags(repartition_tags).ids
                    for tax_res in balance_taxes_res['taxes']:
                        tax_res['tag_ids'] = base_line._revert_signed_tags(self.env['account.account.tag'].browse(tax_res['tag_ids'])).ids

            return balance_taxes_res

        taxes_map = {}

        # ==== Add tax lines ====
        to_remove = self.env['account.move.line']
        for line in self.line_ids.filtered('tax_repartition_line_id'):
            grouping_dict = self._get_tax_grouping_key_from_tax_line(line)
            grouping_key = _serialize_tax_grouping_key(grouping_dict)
            if grouping_key in taxes_map:
                # A line with the same key does already exist, we only need one
                # to modify it; we have to drop this one.
                to_remove += line
            else:
                taxes_map[grouping_key] = {
                    'tax_line': line,
                    'amount': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                }
        self.line_ids -= to_remove

        # ==== Mount base lines ====
        for line in self.line_ids.filtered(lambda line: not line.tax_repartition_line_id):
            # Don't call compute_all if there is no tax.
            if not line.tax_ids:
                line.tax_tag_ids = [(5, 0, 0)]
                continue

            compute_all_vals = _compute_base_line_taxes(line)

            # Assign tags on base line
            line.tax_tag_ids = compute_all_vals['base_tags'] or [(5, 0, 0)]

            # tax_exigible = True
            for tax_vals in compute_all_vals['taxes']:
                grouping_dict = self._get_tax_grouping_key_from_base_line(line, tax_vals)
                grouping_key = _serialize_tax_grouping_key(grouping_dict)

                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_vals['tax_repartition_line_id'])
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id

                # if tax.tax_exigibility == 'on_payment':
                    # tax_exigible = False

                taxes_map_entry = taxes_map.setdefault(grouping_key, {
                    'tax_line': None,
                    'amount': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                })
                taxes_map_entry['amount'] += tax_vals['amount']
                taxes_map_entry['tax_base_amount'] += self._get_base_amount_to_display(tax_vals['base'], tax_repartition_line, tax_vals['group'])
                taxes_map_entry['grouping_dict'] = grouping_dict
            # line.tax_exigible = tax_exigible

        # ==== Process taxes_map ====
        for taxes_map_entry in taxes_map.values():
            # The tax line is no longer used in any base lines, drop it.
            if taxes_map_entry['tax_line'] and not taxes_map_entry['grouping_dict']:
                self.line_ids -= taxes_map_entry['tax_line']
                continue

            currency = self.env['res.currency'].browse(taxes_map_entry['grouping_dict']['currency_id'])

            # Don't create tax lines with zero balance.
            if currency.is_zero(taxes_map_entry['amount']):
                if taxes_map_entry['tax_line']:
                    self.line_ids -= taxes_map_entry['tax_line']
                continue

            # tax_base_amount field is expressed using the company currency.
            tax_base_amount = currency._convert(taxes_map_entry['tax_base_amount'], self.company_currency_id, self.company_id, self.date or fields.Date.context_today(self))

            # Recompute only the tax_base_amount.
            if taxes_map_entry['tax_line'] and recompute_tax_base_amount:
                taxes_map_entry['tax_line'].tax_base_amount = tax_base_amount
                continue

            balance = currency._convert(
                taxes_map_entry['amount'],
                self.journal_id.company_id.currency_id,
                self.journal_id.company_id,
                self.date or fields.Date.context_today(self),
            )

            analytic_tag_list = []
            others_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
            for rec in others_lines:
                for res in rec.analytic_tag_ids:
                    analytic_tag_list.append(res.id)

            to_write_on_line = {
                'amount_currency': taxes_map_entry['amount'],
                'currency_id': taxes_map_entry['grouping_dict']['currency_id'],
                'debit': balance > 0.0 and balance or 0.0,
                'credit': balance < 0.0 and -balance or 0.0,
                'tax_base_amount': tax_base_amount,
                'analytic_tag_ids': [(6,0,analytic_tag_list)]
            }

            if taxes_map_entry['tax_line']:
                # Update an existing tax line.
                taxes_map_entry['tax_line'].update(to_write_on_line)
            else:
                create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
                tax_repartition_line_id = taxes_map_entry['grouping_dict']['tax_repartition_line_id']
                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_repartition_line_id)
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id
                taxes_map_entry['grouping_dict']['analytic_tag_ids'] = [(6,0,analytic_tag_list)]
                taxes_map_entry['tax_line'] = create_method({
                    **to_write_on_line,
                    'name': tax.name,
                    'move_id': self.id,
                    'partner_id': line.partner_id.id,
                    'company_id': line.company_id.id,
                    'company_currency_id': line.company_currency_id.id,
                    'tax_base_amount': tax_base_amount,
                    'exclude_from_invoice_tab': True,
                    # 'tax_exigible': tax.tax_exigibility == 'on_invoice',
                    **taxes_map_entry['grouping_dict'],
                })

            if in_draft_mode:
                taxes_map_entry['tax_line'].update(taxes_map_entry['tax_line']._get_fields_onchange_balance(force_computation=True))
            
    # @api.depends('line_ids.amount_currency', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id', 'currency_id', 'amount_total', 'amount_untaxed')
    # def _compute_tax_totals_json(self):
    #     """ Computed field used for custom widget's rendering.
    #         Only set on invoices.
    #     """
    #     print("JALAN _compute_tax_totals_json")
    #     for move in self:
    #         if not move.is_invoice(include_receipts=True):
    #             # Non-invoice moves don't support that field (because of multicurrency: all lines of the invoice share the same currency)
    #             move.tax_totals_json = None
    #             continue

    #         tax_lines_data = move._prepare_tax_lines_data_for_totals_from_invoice()

    #         move.tax_totals_json = json.dumps({
    #             **self._get_tax_totals(move.partner_id, tax_lines_data, move.amount_total, move.amount_untaxed, move.currency_id),
    #             'allow_tax_edition': move.is_purchase_document(include_receipts=False) and move.state == 'draft',
    #         })

    # def _prepare_tax_lines_data_for_totals_from_invoice(self, tax_line_id_filter=None, tax_ids_filter=None):
    #     """ Prepares data to be passed as tax_lines_data parameter of _get_tax_totals() from an invoice.

    #         NOTE: tax_line_id_filter and tax_ids_filter are used in l10n_latam to restrict the taxes with consider
    #               in the totals.

    #         :param tax_line_id_filter: a function(aml, tax) returning true if tax should be considered on tax move line aml.
    #         :param tax_ids_filter: a function(aml, taxes) returning true if taxes should be considered on base move line aml.

    #         :return: A list of dict in the format described in _get_tax_totals's tax_lines_data's docstring.
    #     """
    #     self.ensure_one()

    #     tax_line_id_filter = tax_line_id_filter or (lambda aml, tax: True)
    #     tax_ids_filter = tax_ids_filter or (lambda aml, tax: True)

    #     balance_multiplicator = -1 if self.is_inbound() else 1
    #     tax_lines_data = []

    #     print("========== balance_multiplicator ==========", balance_multiplicator)
        
    #     for line in self.line_ids:
            
    #         if line.tax_line_id and tax_line_id_filter(line, line.tax_line_id):
    #             print("========== #1 - TOP ==========")
    #             print("========== LINE.NAME ==========", line.name)
    #             print("========== LINE.AMOUNT_CURRENCY ==========", line.amount_currency)
    #             tax_lines_data.append({
    #                 'line_key': 'tax_line_%s' % line.id,
    #                 'tax_amount': line.amount_currency * balance_multiplicator,
    #                 'tax': line.tax_line_id,
    #             })

    #         if line.tax_ids:
    #             for base_tax in line.tax_ids.flatten_taxes_hierarchy():
    #                 if tax_ids_filter(line, base_tax):
    #                     print("========== #2 - BOT ==========")
    #                     print("========== LINE.NAME ==========", line.name)
    #                     print("========== LINE.AMOUNT_CURRENCY ==========", line.amount_currency)        
                        
    #                     price_unit = line.price_unit
    #                     quantity = line.quantity
    #                     line.sub_total_disc = first_disc = second_disc = third_disc = fourth_disc = 0
    #                     if line.first_disc: #in percentage
    #                         first_disc = (price_unit*quantity) * (line.first_disc / 100.0)
    #                         line.sub_total_disc += first_disc
    #                     if line.second_disc: #in percentage
    #                         second_disc = (price_unit*quantity-first_disc) * (line.second_disc / 100.0)
    #                         line.sub_total_disc += second_disc
    #                     if line.third_disc: #in percentage
    #                         third_disc = (price_unit*quantity-second_disc) * (line.third_disc / 100.0)
    #                         line.sub_total_disc += third_disc
    #                     if line.fourth_disc: #in percentage
    #                         fourth_disc = (price_unit*quantity-third_disc) * (line.fourth_disc / 100.0)
    #                         line.sub_total_disc += fourth_disc

    #                     print("========== AMCUR-SUBTOT ==========", line.amount_currency-line.sub_total_disc)        
                        
    #                     tax_lines_data.append({
    #                         'line_key': 'base_line_%s' % line.id,
    #                         #ORIGINAL: 'base_amount': line.amount_currency * balance_multiplicator,
    #                         'base_amount': (line.amount_currency-line.sub_total_disc) * balance_multiplicator,
    #                         'tax': base_tax,
    #                         'tax_affecting_base': line.tax_line_id,
    #                     })

    #     return tax_lines_data

    # @api.model
    # def _get_tax_totals(self, partner, tax_lines_data, amount_total, amount_untaxed, currency):
    #     """ Compute the tax totals for the provided data.

    #     :param partner:        The partner to compute totals for
    #     :param tax_lines_data: All the data about the base and tax lines as a list of dictionaries.
    #                            Each dictionary represents an amount that needs to be added to either a tax base or amount.
    #                            A tax amount looks like:
    #                                {
    #                                    'line_key':             unique identifier,
    #                                    'tax_amount':           the amount computed for this tax
    #                                    'tax':                  the account.tax object this tax line was made from
    #                                }
    #                            For base amounts:
    #                                {
    #                                    'line_key':             unique identifier,
    #                                    'base_amount':          the amount to add to the base of the tax
    #                                    'tax':                  the tax basing itself on this amount
    #                                    'tax_affecting_base':   (optional key) the tax whose tax line is having the impact
    #                                                            denoted by 'base_amount' on the base of the tax, in case of taxes
    #                                                            affecting the base of subsequent ones.
    #                                }
    #     :param amount_total:   Total amount, with taxes.
    #     :param amount_untaxed: Total amount without taxes.
    #     :param currency:       The currency in which the amounts are computed.

    #     :return: A dictionary in the following form:
    #         {
    #             'amount_total':                              The total amount to be displayed on the document, including every total types.
    #             'amount_untaxed':                            The untaxed amount to be displayed on the document.
    #             'formatted_amount_total':                    Same as amount_total, but as a string formatted accordingly with partner's locale.
    #             'formatted_amount_untaxed':                  Same as amount_untaxed, but as a string formatted accordingly with partner's locale.
    #             'allow_tax_edition':                         True if the user should have the ability to manually edit the tax amounts by group
    #                                                          to fix rounding errors.
    #             'groups_by_subtotals':                       A dictionary formed liked {'subtotal': groups_data}
    #                                                          Where total_type is a subtotal name defined on a tax group, or the default one: 'Untaxed Amount'.
    #                                                          And groups_data is a list of dict in the following form:
    #                                                             {
    #                                                                 'tax_group_name':                  The name of the tax groups this total is made for.
    #                                                                 'tax_group_amount':                The total tax amount in this tax group.
    #                                                                 'tax_group_base_amount':           The base amount for this tax group.
    #                                                                 'formatted_tax_group_amount':      Same as tax_group_amount, but as a string
    #                                                                                                    formatted accordingly with partner's locale.
    #                                                                 'formatted_tax_group_base_amount': Same as tax_group_base_amount, but as a string
    #                                                                                                    formatted accordingly with partner's locale.
    #                                                                 'tax_group_id':                    The id of the tax group corresponding to this dict.
    #                                                                 'group_key':                       A unique key identifying this total dict,
    #                                                             }
    #             'subtotals':                                 A list of dictionaries in the following form, one for each subtotal in groups_by_subtotals' keys
    #                                                             {
    #                                                                 'name':                            The name of the subtotal
    #                                                                 'amount':                          The total amount for this subtotal, summing all
    #                                                                                                    the tax groups belonging to preceding subtotals and the base amount
    #                                                                 'formatted_amount':                Same as amount, but as a string
    #                                                                                                    formatted accordingly with partner's locale.
    #                                                             }
    #         }
    #     """
    #     account_tax = self.env['account.tax']

    #     grouped_taxes = defaultdict(lambda: defaultdict(lambda: {'base_amount': 0.0, 'tax_amount': 0.0, 'base_line_keys': set()}))
    #     subtotal_priorities = {}
    #     for line_data in tax_lines_data:
    #         tax_group = line_data['tax'].tax_group_id

    #         # Update subtotals priorities
    #         if tax_group.preceding_subtotal:
    #             subtotal_title = tax_group.preceding_subtotal
    #             new_priority = tax_group.sequence
    #         else:
    #             # When needed, the default subtotal is always the most prioritary
    #             subtotal_title = _("Untaxed Amount")
    #             new_priority = 0

    #         if subtotal_title not in subtotal_priorities or new_priority < subtotal_priorities[subtotal_title]:
    #             subtotal_priorities[subtotal_title] = new_priority

    #         # Update tax data
    #         tax_group_vals = grouped_taxes[subtotal_title][tax_group]

    #         if 'base_amount' in line_data:
    #             # Base line
    #             if tax_group == line_data.get('tax_affecting_base', account_tax).tax_group_id:
    #                 # In case the base has a tax_line_id belonging to the same group as the base tax,
    #                 # the base for the group will be computed by the base tax's original line (the one with tax_ids and no tax_line_id)
    #                 continue

    #             if line_data['line_key'] not in tax_group_vals['base_line_keys']:
    #                 # If the base line hasn't been taken into account yet, at its amount to the base total.
    #                 tax_group_vals['base_line_keys'].add(line_data['line_key'])
    #                 tax_group_vals['base_amount'] += line_data['base_amount']

    #         else:
    #             # Tax line
    #             tax_group_vals['tax_amount'] += line_data['tax_amount']

    #     # Compute groups_by_subtotal
    #     groups_by_subtotal = {}
    #     for subtotal_title, groups in grouped_taxes.items():
    #         groups_vals = [{
    #             'tax_group_name': group.name,
    #             'tax_group_amount': amounts['tax_amount'],
    #             'tax_group_base_amount': amounts['base_amount'],
    #             'formatted_tax_group_amount': formatLang(self.env, amounts['tax_amount'], currency_obj=currency),
    #             'formatted_tax_group_base_amount': formatLang(self.env, amounts['base_amount'], currency_obj=currency),
    #             'tax_group_id': group.id,
    #             'group_key': '%s-%s' %(subtotal_title, group.id),
    #         } for group, amounts in sorted(groups.items(), key=lambda l: l[0].sequence)]

    #         groups_by_subtotal[subtotal_title] = groups_vals

    #     # Compute subtotals
    #     subtotals_list = [] # List, so that we preserve their order
    #     previous_subtotals_tax_amount = 0
    #     for subtotal_title in sorted((sub for sub in subtotal_priorities), key=lambda x: subtotal_priorities[x]):
    #         subtotal_value = amount_untaxed + previous_subtotals_tax_amount
    #         subtotals_list.append({
    #             'name': subtotal_title,
    #             'amount': subtotal_value,
    #             'formatted_amount': formatLang(self.env, subtotal_value, currency_obj=currency),
    #         })

    #         subtotal_tax_amount = sum(group_val['tax_group_amount'] for group_val in groups_by_subtotal[subtotal_title])
    #         previous_subtotals_tax_amount += subtotal_tax_amount

    #     # Assign json-formatted result to the field
    #     return {
    #         'amount_total': amount_total,
    #         'amount_untaxed': amount_untaxed,
    #         'formatted_amount_total': formatLang(self.env, amount_total, currency_obj=currency),
    #         'formatted_amount_untaxed': formatLang(self.env, amount_untaxed, currency_obj=currency),
    #         'groups_by_subtotal': groups_by_subtotal,
    #         'subtotals': subtotals_list,
    #         'allow_tax_edition': False,
    #     }

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #     for node in doc.xpath("//field[@name='partner_id']"):
    #         print("JOURNAL_NAME => ", self.journal_id.type)
    #         if self.journal_id.type == 'sale': #_context.get('sale'):
    #             node.set('domain', "['customer_rank','>',0]")
    #         else:
    #             node.set('domain', "['supplier_rank','>',0]")
    #     return res        
    
    # @api.onchange('journal_id')
    # def _onchange_journal_id(self):
    #     print("_onchange_journal_id => ", self.journal_id.type)
            

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    first_disc = fields.Float('Disc % (1)')
    second_disc = fields.Float('Disc % (2)')
    third_disc = fields.Float('Disc % (3)')
    fourth_disc = fields.Float('Disc % (4)')
    sub_total_disc = fields.Monetary(string='Total Disc.', compute="_compute_subtotal_disc", store=True, default=0.0)
    
    line_move_type = fields.Char(compute='_compute_line_move_type', string='Move Type')
    
    @api.depends('move_id.move_type')
    def _compute_line_move_type(self):
        for me in self:
            me.line_move_type = me.move_id.move_type
    
    line_is_new_purchase = fields.Boolean(compute='_compute_line_is_new_purchase', string='Line: Is New Purchase?', store=True)
    
    @api.depends('move_id.is_new_purchase')
    def _compute_line_is_new_purchase(self):
        for me in self:
            me.line_is_new_purchase = me.move_id.is_new_purchase
    
    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        # ACCOUNTING_FIELDS = ('debit', 'credit', 'amount_currency')
        # BUSINESS_FIELDS = ('price_unit', 'quantity', 'discount', 'tax_ids')

        for vals in vals_list:
            move = self.env['account.move'].browse(vals['move_id'])
            vals.setdefault('company_currency_id', move.company_id.currency_id.id) # important to bypass the ORM limitation where monetary fields are not rounded; more info in the commit message

            # Ensure balance == amount_currency in case of missing currency or same currency as the one from the company.
            currency_id = vals.get('currency_id') or move.company_id.currency_id.id
            if currency_id == move.company_id.currency_id.id:
                balance = vals.get('debit', 0.0) - vals.get('credit', 0.0)
                vals.update({
                    'currency_id': currency_id,
                    'amount_currency': balance,
                })
            else:
                vals['amount_currency'] = vals.get('amount_currency', 0.0)

            if move.is_invoice(include_receipts=True):
                # currency = move.currency_id
                # partner = self.env['res.partner'].browse(vals.get('partner_id'))
                taxes = self.new({'tax_ids': vals.get('tax_ids', [])}).tax_ids
                tax_ids = set(taxes.ids)
                taxes = self.env['account.tax'].browse(tax_ids)

        lines = super(models.Model, self).create(vals_list)

        moves = lines.mapped('move_id')
        if self._context.get('check_move_validity', True):
            moves._check_balanced()
        moves._check_fiscalyear_lock_date()
        lines._check_tax_lock_date()
        moves._synchronize_business_models({'line_ids'})

        return lines

    @api.onchange(
        "discount",
        "price_unit",
        "tax_ids",
        "quantity",
        "first_disc",
        "second_disc",
        "third_disc",
        "fourth_disc"
    )
    def _onchange_price_subtotal(self):
        return super(AccountMoveLine, self)._onchange_price_subtotal()

    # @api.onchange('amount_currency', 'currency_id', 'debit', 'credit', 'tax_ids', 'account_id', 'first_disc', 'second_disc', 'third_disc', 'fourth_disc')
    # def _onchange_mark_recompute_taxes(self):
    #     return super(AccountMoveLine, self)._onchange_mark_recompute_taxes()

    @api.depends('price_unit','quantity','first_disc','second_disc','third_disc','fourth_disc')
    def _compute_subtotal_disc(self):
        for line in self:
            price_unit = line.price_unit
            quantity = line.quantity
            line.sub_total_disc = first_disc = second_disc = third_disc = fourth_disc = 0
            initial_price = current_price = price_unit*quantity
            if line.first_disc: #in percentage
                first_disc = (current_price) * (line.first_disc / 100.0)
                print(">>>>>>>>>> first_disc", first_disc)
                line.sub_total_disc += first_disc
                current_price -= first_disc
            if line.second_disc: #in percentage
                second_disc = (current_price) * (line.second_disc / 100.0)
                print(">>>>>>>>>> second_disc", second_disc)
                line.sub_total_disc += second_disc
                current_price -= second_disc
            if line.third_disc: #in percentage
                third_disc = (current_price) * (line.third_disc / 100.0)
                print(">>>>>>>>>> third_disc", third_disc)
                line.sub_total_disc += third_disc
                current_price -= third_disc
            if line.fourth_disc: #in percentage
                fourth_disc = (current_price) * (line.fourth_disc / 100.0)
                print(">>>>>>>>>> fourth_disc", fourth_disc)
                line.sub_total_disc += fourth_disc
                current_price -= third_disc

    @api.model
    def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):
        ''' This method is used to recompute the values of 'amount_currency', 'debit', 'credit' due to a change made
        in some business fields (affecting the 'price_subtotal' field).

        :param price_subtotal:  The untaxed amount.
        :param move_type:       The type of the move.
        :param currency:        The line's currency.
        :param company:         The move's company.
        :param date:            The move's date.
        :return:                A dictionary containing 'debit', 'credit', 'amount_currency'.
        '''
        if move_type in self.move_id.get_outbound_types():
            sign = 1
        elif move_type in self.move_id.get_inbound_types():
            sign = -1
        else:
            sign = 1

        amount_currency = (price_subtotal + self.sub_total_disc) * sign # SUBTOTAL BEFORE DISCOUNT
        balance = currency._convert(amount_currency, company.currency_id, company, date or fields.Date.context_today(self))
        return {
            'amount_currency': amount_currency,
            'currency_id': currency.id,
            'debit': balance > 0.0 and balance or 0.0,
            'credit': balance < 0.0 and -balance or 0.0,
        }

    def _get_price_total_and_subtotal(self, price_unit=None, quantity=None, discount=None, currency=None, product=None, partner=None, taxes=None, move_type=None):
        self.ensure_one()
        if self.sub_total_disc and self.quantity:
            price_unit = price_unit - (self.sub_total_disc/self.quantity) if price_unit else self.price_unit - (self.sub_total_disc/self.quantity)
        else:
            price_unit = self.price_unit
        return self._get_price_total_and_subtotal_model(
            price_unit=price_unit,
            quantity=quantity or self.quantity,
            discount=discount or self.discount,
            currency=currency or self.currency_id,
            product=product or self.product_id,
            partner=partner or self.partner_id,
            taxes=taxes or self.tax_ids,
            move_type=move_type or self.move_id.move_type,
        )

    @api.model
    def _get_fields_onchange_balance_model(self, quantity, discount, amount_currency, move_type, currency, taxes, price_subtotal, force_computation=False):
        ''' This method is used to recompute the values of 'quantity', 'discount', 'price_unit' due to a change made
        in some accounting fields such as 'balance'.

        This method is a bit complex as we need to handle some special cases.
        For example, setting a positive balance with a 100% discount.

        :param quantity:        The current quantity.
        :param discount:        The current discount.
        :param amount_currency: The new balance in line's currency.
        :param move_type:       The type of the move.
        :param currency:        The currency.
        :param taxes:           The applied taxes.
        :param price_subtotal:  The price_subtotal.
        :return:                A dictionary containing 'quantity', 'discount', 'price_unit'.
        '''
        if move_type in self.move_id.get_outbound_types():
            sign = 1
        elif move_type in self.move_id.get_inbound_types():
            sign = -1
        else:
            sign = 1
        amount_currency *= sign

        # Avoid rounding issue when dealing with price included taxes. For example, when the price_unit is 2300.0 and
        # a 5.5% price included tax is applied on it, a balance of 2300.0 / 1.055 = 2180.094 ~ 2180.09 is computed.
        # However, when triggering the inverse, 2180.09 + (2180.09 * 0.055) = 2180.09 + 119.90 = 2299.99 is computed.
        # To avoid that, set the price_subtotal at the balance if the difference between them looks like a rounding
        # issue.
        if not force_computation and currency.is_zero(amount_currency - price_subtotal):
            return {}

        taxes = taxes.flatten_taxes_hierarchy()
        if taxes and any(tax.price_include for tax in taxes):
            # Inverse taxes. E.g:
            #
            # Price Unit    | Taxes         | Originator Tax    |Price Subtotal     | Price Total
            # -----------------------------------------------------------------------------------
            # 110           | 10% incl, 5%  |                   | 100               | 115
            # 10            |               | 10% incl          | 10                | 10
            # 5             |               | 5%                | 5                 | 5
            #
            # When setting the balance to -200, the expected result is:
            #
            # Price Unit    | Taxes         | Originator Tax    |Price Subtotal     | Price Total
            # -----------------------------------------------------------------------------------
            # 220           | 10% incl, 5%  |                   | 200               | 230
            # 20            |               | 10% incl          | 20                | 20
            # 10            |               | 5%                | 10                | 10
            force_sign = -1 if move_type in ('out_invoice', 'in_refund', 'out_receipt') else 1
            taxes_res = taxes._origin.with_context(force_sign=force_sign).compute_all(amount_currency, currency=currency, handle_price_include=False)
            for tax_res in taxes_res['taxes']:
                tax = self.env['account.tax'].browse(tax_res['id'])
                if tax.price_include:
                    amount_currency += tax_res['amount']

        discount_factor = 1 - (discount / 100.0)
        if amount_currency and discount_factor:
            # discount != 100%
            vals = {
                'quantity': quantity or 1.0,
                # 'price_unit': amount_currency / discount_factor / (quantity or 1.0),
            }
        elif amount_currency and not discount_factor:
            # discount == 100%
            vals = {
                'quantity': quantity or 1.0,
                'discount': 0.0,
                # 'price_unit': amount_currency / (quantity or 1.0),
            }
        elif not discount_factor:
            # balance of line is 0, but discount  == 100% so we display the normal unit_price
            vals = {}
        else:
            # balance is 0, so unit price is 0 as well
            vals = {'price_unit': 0.0}
        return vals

    @api.onchange('first_disc', 'second_disc', 'third_disc', 'fourth_disc')
    def _onchange_discs(self):
        print("JALAN! _onchange_discs")
        for line in self:
            line.recompute_tax_line = True
            # taxes = line._get_computed_taxes()
            # if taxes and line.move_id.fiscal_position_id:
            #     taxes = line.move_id.fiscal_position_id.map_tax(taxes)
            # line.tax_ids = taxes
            