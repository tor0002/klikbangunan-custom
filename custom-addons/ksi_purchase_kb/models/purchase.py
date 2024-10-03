from bdb import effective
import json
from odoo import _, api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = 'Purchase Order (inherited by ksi_purchase_kb)'
    
    first_note = fields.Text('1st Note')
    second_note = fields.Text('2nd Note')
    
    amount_after_disc = fields.Monetary('Amount after Discount', compute="_compute_after_disc")
    
    selisih_hari = fields.Text(string="Selisih Hari", compute="_get_selisih_hari")
    active = fields.Boolean(string='Active', default=True)

    # def button_confirm(self):
    #     res = super(PurchaseOrder, self).button_confirm()
    #     for picking in self.picking_ids:
    #         for move in picking.move_ids_without_package:
    #             move.custom_weight = move.purchase_line_id.custom_weight
    #             move.total_weight = move.purchase_line_id.total_weight
    #     return res

    @api.depends('amount_untaxed')
    def _compute_after_disc(self):
        for rec in self : 
            # if rec.global_discount:
            #     discount = rec.amount_untaxed * rec.global_discount / 100.0
            #     rec.amount_after_disc = rec.amount_untaxed - discount
            #     rec.amount_total = rec.amount_after_disc + rec.amount_tax
            # else:
            #     rec.amount_after_disc = 0.0
            rec.amount_after_disc = 0.0

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                print("AMOUNT_UNTAXED", amount_untaxed)
                amount_tax += line.price_tax
                print("AMOUNT_TAX", amount_tax)
            currency = order.currency_id or order.partner_id.property_purchase_currency_id or self.env.company.currency_id
            order.update({
                'amount_untaxed': currency.round(amount_untaxed),
                'amount_tax': currency.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.depends('order_line.taxes_id', 'order_line.price_subtotal', 'amount_total', 'amount_untaxed')
    def  _compute_tax_totals_json(self):
        def compute_taxes(order_line):
            unit_price = order_line.price_unit
            unit_qty = order_line.product_qty
            sub_total_price = unit_qty * unit_price
            
            amount_disc = 0.0
            sub_total_disc = 0.0
            price = 0.0
            
            diskon_kesatu = order_line.first_disc
            diskon_kedua = order_line.second_disc
            diskon_ketiga = order_line.third_disc
            diskon_keempat = order_line.fourth_disc
            
            #1. Pengecekan apakah Diskon Persenan (1) ada di antara 0 dan 100?
            if diskon_kesatu < 0.0 or diskon_kesatu > 100.0:
                raise ValidationError("PERHATIAN: Disc % (1) tidak boleh kurang dari 0 atau lebih dari 100!")

            #2. Pengecekan apakah Diskon Persenan (2) ada di antara 0 dan 100?
            if diskon_kedua < 0.0 or diskon_kedua > 100.0:
                raise ValidationError("PERHATIAN: Disc % (2) tidak boleh kurang dari 0 atau lebih dari 100!")

            #3. Pengecekan apakah Diskon Persenan (3) ada di antara 0 dan 100?
            if diskon_ketiga < 0.0 or diskon_ketiga > 100.0:
                raise ValidationError("PERHATIAN: Disc % (3) tidak boleh kurang dari 0 atau lebih dari 100!")

            #4. Pengecekan apakah Diskon Persenan (4) ada di antara 0 dan 100?
            if diskon_keempat < 0.0 or diskon_keempat > 100.0:
                raise ValidationError("PERHATIAN: Disc % (4) tidak boleh kurang dari 0 atau lebih dari 100!")
            
            #1. Hitung Diskon Persenan ke-1
            amount_disc = (sub_total_price * diskon_kesatu) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc
            
            #2. Hitung Diskon Persenan ke-2
            amount_disc = (sub_total_price * diskon_kedua) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc
            
            #3. Hitung Diskon Persenan ke-3
            amount_disc = (sub_total_price * diskon_ketiga) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc
            
            #4. Hitung Diskon Persenan ke-4
            amount_disc = (sub_total_price * diskon_keempat) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc
            
            price = sub_total_price
            print("price", price)
            order_line.price_subtotal = price
            
            # taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
            
            vals = order_line._prepare_compute_all_values()
            taxes = order_line.taxes_id._origin.compute_all(
                price,
                vals['currency'],
                1,
                vals['product'],
                vals['partner'])
            return taxes
            # return order_line.taxes_id._origin.compute_all(**order_line._prepare_compute_all_values())

        account_move = self.env['account.move']
        for order in self:
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
            order.tax_totals_json = json.dumps(tax_totals)
            
    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        move_type = self._context.get('default_move_type', 'in_invoice')
        journal = self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting purchase journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        partner_invoice_id = self.partner_id.address_get(['invoice'])['invoice']
        partner_bank_id = self.partner_id.bank_ids.filtered_domain(['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]
        invoice_vals = {
            'ref': self.partner_ref or '',
            'move_type': move_type,
            'narration': self.notes,
            'currency_id': self.currency_id.id,
            'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
            'partner_id': partner_invoice_id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(partner_invoice_id)).id,
            'payment_reference': self.partner_ref or '',
            'partner_bank_id': partner_bank_id.id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            'amount_after_disc': self.amount_after_disc
        }
        print('<<<<<<< invoice_vals >>>>>>>', invoice_vals)
        return invoice_vals

    @api.depends('date_approve','effective_date')
    def _get_selisih_hari(self):
        for rec in self:
            if not rec.effective_date:
                rec.selisih_hari = "0:00:00"
            else:
                effective = rec.effective_date.date()
                approve = rec.date_approve.date()
                selisih = effective - approve
                rec.selisih_hari = selisih

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    first_disc = fields.Float('Disc % (1)')
    second_disc = fields.Float('Disc % (2)')
    third_disc = fields.Float('Disc % (3)')
    fourth_disc = fields.Float('Disc % (4)')
    #custom
    custom_weight = fields.Float('Weight', related='product_id.weight')
    total_weight = fields.Float('Total Weight',compute='_compute_custom_weight')

    @api.depends('custom_weight','product_qty')
    def _compute_custom_weight(self):
        for line in self:
            line.total_weight = line.custom_weight * line.product_qty

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'first_disc', 'second_disc', 'third_disc', 'fourth_disc')
    def _compute_amount(self):
        for line in self:
            unit_price = line.price_unit
            unit_qty = line.product_qty
            sub_total_price = unit_qty * unit_price
            
            amount_disc = 0.0
            sub_total_disc = 0.0
            price = 0.0
            
            diskon_kesatu = line.first_disc
            diskon_kedua = line.second_disc
            diskon_ketiga = line.third_disc
            diskon_keempat = line.fourth_disc
            
            #1. Pengecekan apakah Diskon Persenan (1) ada di antara 0 dan 100?
            if diskon_kesatu < 0.0 or diskon_kesatu > 100.0:
                raise ValidationError("PERHATIAN: Disc % (1) tidak boleh kurang dari 0 atau lebih dari 100!")

            #2. Pengecekan apakah Diskon Persenan (2) ada di antara 0 dan 100?
            if diskon_kedua < 0.0 or diskon_kedua > 100.0:
                raise ValidationError("PERHATIAN: Disc % (2) tidak boleh kurang dari 0 atau lebih dari 100!")

            #3. Pengecekan apakah Diskon Persenan (3) ada di antara 0 dan 100?
            if diskon_ketiga < 0.0 or diskon_ketiga > 100.0:
                raise ValidationError("PERHATIAN: Disc % (3) tidak boleh kurang dari 0 atau lebih dari 100!")

            #4. Pengecekan apakah Diskon Persenan (4) ada di antara 0 dan 100?
            if diskon_keempat < 0.0 or diskon_keempat > 100.0:
                raise ValidationError("PERHATIAN: Disc % (4) tidak boleh kurang dari 0 atau lebih dari 100!")
            
            #1. Hitung Diskon Persenan ke-1
            amount_disc = (sub_total_price * diskon_kesatu) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc
            
            #2. Hitung Diskon Persenan ke-2
            amount_disc = (sub_total_price * diskon_kedua) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc
            
            #3. Hitung Diskon Persenan ke-3
            amount_disc = (sub_total_price * diskon_ketiga) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc
            
            #4. Hitung Diskon Persenan ke-4
            amount_disc = (sub_total_price * diskon_keempat) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc
            
            price = sub_total_price
            print("price", price)
            line.price_subtotal = price
            
            # taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
            
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                price,
                vals['currency'],
                1,
                vals['product'],
                vals['partner'])
            print("taxes['total_included']", taxes['total_included'])
            print("taxes['total_excluded']", taxes['total_excluded'])
            
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])), #taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        return {
            'price_unit': self.price_unit,
            'currency': self.order_id.currency_id,
            'quantity': self.product_qty,
            'product': self.product_id,
            'partner': self.order_id.partner_id,
        }
        
    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': '%s: %s' % (self.order_id.name, self.name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'purchase_line_id': self.id,
            'first_disc' : self.first_disc,
            'second_disc' : self.second_disc,
            'third_disc' : self.third_disc,
            'fourth_disc' : self.fourth_disc
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update({
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'date_maturity': move.invoice_date_due,
            'partner_id': move.partner_id.id,
        })
        return res