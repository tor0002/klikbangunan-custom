# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    _description = "Point of Sale Orders Report (inherited by 'ksi_pos')"

    margin_percent = fields.Float('Margin %', group_operator="avg")
    
    customer_state = fields.Many2one('res.country.state','Location')
    media_akuisisi = fields.Many2one('media.acquisition','Media Akuisisi')
    # customer_category = fields.Char('Jenis Member Char',related="partner_id.tags")
    # product_category = fields.Char('Parent Category',related="product_id.categ_id.parent_id.name", store=True)
    # category_ids = fields.Many2many('res.partner.category', string='Jenis Member',relation='pos_category_rel',column1='pos_category_id',column2='category_pos_id', related='partner_id.category_id', store=True)
    tags = fields.Char('Jenis Member')
    # categ_id = fields.Many2one('product.category', string='Parent Category')
    # tukang = fields.Char('Tukang')
    parent_category = fields.Char('Parent Category')

    # ! OVERRIDE
    def _select(self):
        # print("SELECT!!!")
        return """
            SELECT
                MIN(l.id) AS id,
                COUNT(*) AS nbr_lines,
                s.date_order AS date,
                SUM(l.qty) AS product_qty,
                SUM(l.qty * l.price_unit / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_sub_total,
                SUM(ROUND((l.qty * l.price_unit) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END, cu.decimal_places)) AS price_total,
                SUM((l.qty * l.price_unit) * (l.discount / 100) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS total_discount,
                CASE
                    WHEN SUM(l.qty * u.factor) = 0 THEN NULL
                    ELSE (SUM(l.qty*l.price_unit / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)/SUM(l.qty * u.factor))::decimal
                END AS average_price,
                SUM(cast(to_char(date_trunc('day',s.date_order) - date_trunc('day',s.create_date),'DD') AS INT)) AS delay_validation,
                s.id as order_id,
                s.partner_id AS partner_id,
                s.state AS state,
                s.user_id AS user_id,
                s.company_id AS company_id,
                s.sale_journal AS journal_id,
                l.product_id AS product_id,
                pt.categ_id AS product_categ_id,
                p.product_tmpl_id,
                ps.config_id,
                pt.pos_categ_id,
                s.pricelist_id,
                s.session_id,
                rs.media_acquisition_id AS media_akuisisi,
                rs.state_id AS customer_state,
                rs.tags AS tags,
                pt.parrent_category AS parent_category,
                s.employee_id AS employee_id,
                s.account_move IS NOT NULL AS invoiced,
                SUM(l.price_subtotal - l.total_cost / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS margin,
                CASE WHEN l.product_id IS NOT NULL THEN (case when sum(l.price_subtotal) != 0 and avg(l.total_cost * l.qty) < sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) then AVG(l.price_subtotal - l.total_cost / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)/sum(l.price_subtotal) else 0.0 end) * 100.0 ELSE 0.0 END AS margin_percent
        """
    def _from(self):
        return """
            FROM pos_order_line AS l
                INNER JOIN pos_order s ON (s.id=l.order_id)
                LEFT JOIN product_product p ON (l.product_id=p.id)
                LEFT JOIN product_template pt ON (p.product_tmpl_id=pt.id)
                LEFT JOIN uom_uom u ON (u.id=pt.uom_id)
                LEFT JOIN pos_session ps ON (s.session_id=ps.id)
                LEFT JOIN res_company co ON (s.company_id=co.id)
                LEFT JOIN res_currency cu ON (co.currency_id=cu.id)
                LEFT JOIN res_partner rs ON (rs.id=s.partner_id)

        """
    
    def _group_by(self):
        return """
            GROUP BY
                s.id, s.date_order, s.partner_id,s.state, pt.categ_id,
                s.user_id, s.company_id, s.sale_journal,
                s.pricelist_id, s.account_move, s.create_date, s.session_id,
                l.product_id,
                pt.categ_id, pt.pos_categ_id,
                p.product_tmpl_id,
                ps.config_id,
                rs.media_acquisition_id,
                rs.state_id,
                rs.tags,
                pt.parrent_category,
                s.employee_id
        """

class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'
    
    pos_category_ids = fields.Many2many('report.pos.order', string='category',relation='pos_category_rel',column1='category_pos_id',column2='pos_category_id')


