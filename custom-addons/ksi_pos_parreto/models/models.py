# -*- coding: utf-8 -*-

from odoo import models, fields, api
from collections import OrderedDict
import operator
import datetime


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
#     _order = 'price_subtotal_incl desc'

    # percentage = fields.Float('Percentage', compute='_compute_percentage', group_operator=True)
    # total_percentage = fields.Float('Total Percentage', compute='_compute_total_percentage')
    # akumulasi_percentage = fields.Float('Akumulasi Percentage', compute='_compute_akumulasi_percentage')
    # evaluation = fields.Selection([
    #     ('very_fast', 'Very Fast'),
    #     ('fast', 'Fast'),
    #     ('slow', 'Slow')
    # ], 'Evaluation', compute='_compute_evaluation')

    # @api.depends('price_subtotal_incl')
    # def _compute_percentage(self):
    #     for rec in self:
    #         domain = []  # Tentukan domain yang sesuai untuk filtering
    #         print('dito check domain>>>>>>>>>>>>',domain)
    #         filtered_records = self.filtered_domain(domain)
    #         total = sum(filtered_records.mapped('price_subtotal_incl'))
    #         percent = rec.price_subtotal_incl / total * 100 if total else 0.0
    #         rec.percentage = percent


    # @api.depends('price_subtotal_incl')
    # def _compute_percentage(self):
    #     for rec in self:
    #         filter_domain = self.env.context.get('domain', [])
    #         filtered_records = self.filtered(lambda r: all(
    #             eval(expr, {'rec': r}) for expr in filter_domain))
    #         total = sum(filtered_records.mapped('price_subtotal_incl'))
    #         percent = rec.price_subtotal_incl / total * 100 if total else 0.0
    #         rec.percentage = percent


    # @api.depends('price_subtotal_incl')
    # def _compute_percentage(self):
    #     for rec in self:
    #         total = sum(rec.search([]).mapped('price_subtotal_incl'))
    #         print('dito check total>>>>>>>>>>>>>>>>>',total)
    #         percent = rec.price_subtotal_incl/total * 100
    #         rec.percentage = percent

    # @api.depends('percentage')
    # def _compute_total_percentage(self):
    #     for record in self:
    #         same_product_records = self.filtered(
    #             lambda r: r.product_id == record.product_id)
    #         total_percentage = sum(same_product_records.mapped('percentage'))
    #         same_product_records.update({'total_percentage': total_percentage})

    # def _get_filter_domain(self):
    #     today = datetime.datetime.now().date()
    #     domain = [('create_date', '>=', datetime.datetime(2023, 1, 1, 0, 0, 0)),
    #             ('create_date', '<=', datetime.datetime.combine(today, datetime.time(23, 59, 59)))]

    #     if self._context.get('start_date') and self._context.get('end_date'):
    #         start_date = self._context['start_date']
    #         end_date = self._context['end_date']
    #         domain = [('create_date', '>=', start_date),
    #                 ('create_date', '<=', end_date)]

    #     return domain

    # @api.depends('total_percentage')
    # def _compute_akumulasi_percentage(self):
    #     # domain = self._get_filter_domain()
    #     # all_records = self.search(domain)
    #     all_records = self.env['pos.order.line'].search([])
    #     print('dito check all records >>>>>>>>>>>>>>>>>>>>>>', all_records)
    #     sorted_records = sorted(all_records, key=lambda r: r.total_percentage, reverse=True)
    #     # sorted_records = all_records.sorted(key=lambda r: r.total_percentage, reverse=True)
    #     # print('dito check sorted record >>>>>>>>>>>>>>>>>>>>>>', sorted_records)
    #     akumulasi = []
    #     total = 0.0
    #     previous_percentage = None
    #     for record in sorted_records:
    #         if record.total_percentage == previous_percentage:
    #             total += 0  # Jika nilai total_percentage sama, tambahkan dengan 0
    #         else:
    #             total += record.total_percentage

    #         akumulasi.append(total)
    #         # print('dito check total >>>>>>>>>>>>>>>>>>>>>>', total)

    #         previous_percentage = record.total_percentage

    #     # print('dito check akumulasi >>>>>>>>>>>>>>>>>>>>>>', akumulasi)

    #     for index, record in enumerate(sorted_records):
    #         record.akumulasi_percentage = akumulasi[index]


    # @api.depends('akumulasi_percentage')
    # def _compute_evaluation(self):
    #     for rec in self:
    #         if rec.akumulasi_percentage < 50.0:
    #             rec.evaluation = 'very_fast'
    #         elif rec.akumulasi_percentage > 50.0 and rec.akumulasi_percentage < 70.0:
    #             rec.evaluation = 'fast'
    #         elif rec.akumulasi_percentage > 70.0 and rec.akumulasi_percentage < 100.0:
    #             rec.evaluation = 'slow'
    #         else: 
    #             rec.evaluation = 'slow'

    # def action_change(self):

    #     parreto = self.evaluation
    #     print('dito check parreto>>>>>>>>>>>>>>>>>', parreto)
    #     product = self.product_id
    #     print('dito check parreto>>>>>>>>>>>>>>>>>', product)
    #     if product:    
    #         product_products = self.env['product.product'].search([('id','=',product.id)])
    #         product_products.parreto = parreto

    # def action_change_all(self):
    #     all_records = self.env['pos.order.line'].search([])

    #     product_model = self.env['product.product']
    #     for record in all_records:
    #         product = product_model.search(
    #             [('id', '=', record.product_id.id)], limit=1)
    #         if product:
    #             product.parreto = record.evaluation




class ProductTemplate(models.Model):
    _inherit = 'product.template'

    parreto = fields.Char('Parreto')