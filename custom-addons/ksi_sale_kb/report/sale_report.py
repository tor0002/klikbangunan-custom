# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    margin_percent = fields.Float('Margin %', group_operator="avg")
    product_cost = fields.Float('Product Cost', readonly=True)
    # on_hand_qty = fields.Float('On-Hand Qty', group_operator="avg", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        
        fields['margin_percent'] = ", AVG(l.margin_percent) AS margin_percent"
        fields['product_cost'] = ", CASE WHEN l.product_id IS NOT NULL THEN SUM(l.product_cost * l.product_uom_qty) ELSE 0 END AS product_cost"
        # fields['on_hand_qty'] = ", CASE WHEN l.product_id IS NOT NULL THEN AVG(l.on_hand_qty) ELSE 0 END as on_hand_qty"
        
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)