from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Product (inherited by ksi_stock_kb)'

class InheritSupplierInfo(models.Model):
    _name = 'product.supplierinfo'
    _inherit = ['product.supplierinfo', 'mail.thread', 'mail.activity.mixin']
    _description = 'Product Supplierinfo (inherited by ksi_stock_kb)'

    def _default_pricelist(self):
        ProductPricelist = self.env["product.pricelist"].search([])
        return ProductPricelist[0]

    name = fields.Many2one(tracking=True)
    delay = fields.Integer(tracking=True)
    product_tmpl_id = fields.Many2one(tracking=True)
    min_qty = fields.Float(tracking=True)
    price = fields.Float(tracking=True)
    date_start = fields.Date(tracking=True)
    company_id = fields.Many2one(tracking=True)

    # ! Tarik dulu
    margin_ho = fields.Float('Margin HO',tracking=True)
    margin_toko = fields.Float('Margin Toko',tracking=True)
    product_pricelist_id = fields.Many2one('product.pricelist', string='Product Pricelist',tracking=True)
    sales_price = fields.Float(compute='_compute_sales_price', string='Sales Price', store=True,tracking=True)
    sales_price_before = fields.Float(compute="_compute_sales_price_before",string='Current Sales Price',tracking=True,store=True)
    
    #diskon bertingkat
    price_before_discount = fields.Float('Price Before Discount')
    first_discount = fields.Float('First Discount')
    second_discount = fields.Float('Second Discount')
    third_discount = fields.Float('Third Discount')
    fourth_discount = fields.Float('Fourth Discount')
    fifth_discount = fields.Float('Fifth Discount')
    price_after_discount = fields.Float(string='Price After Discount', compute="_compute_discount")

    @api.depends('price_before_discount', 'price_after_discount', 'first_discount', 'second_discount', 'third_discount', 'fourth_discount', 'fifth_discount')
    def _compute_discount(self):
        for rec in self:
            price_before = rec.price_before_discount

            sub_total_price = price_before
            amount_disc = 0.0
            sub_total_disc = 0.0
            price = 0.0

            diskon_kesatu = rec.first_discount
            diskon_kedua = rec.second_discount
            diskon_ketiga = rec.third_discount
            diskon_keempat = rec.fourth_discount
            diskon_kelima = rec.fifth_discount
            # price_after = rec.price_after_discount

            
            print("Dito check >>>>>>>>xxxx>>>>>>", price_before)
            print("Dito check >>>>>>>>xxxx>>>>>>", diskon_kesatu)
            print("Dito check >>>>>>>>xxxx>>>>>>", diskon_kedua)
            print("Dito check >>>>>>>>xxxx>>>>>>", diskon_ketiga)
            print("Dito check >>>>>>>>xxxx>>>>>>", diskon_keempat)
            print("Dito check >>>>>>>>xxxx>>>>>>", diskon_kelima)
            # print("Dito check >>>>>>>>xxxx>>>>>>", price_after)

            amount_disc = (sub_total_price * diskon_kesatu) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc

            amount_disc = (sub_total_price * diskon_kedua) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc

            amount_disc = (sub_total_price * diskon_ketiga) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc

            amount_disc = (sub_total_price * diskon_keempat) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc

            amount_disc = (sub_total_price * diskon_kelima) / 100.0
            sub_total_disc += amount_disc
            sub_total_price -= amount_disc

            price = sub_total_price

            rec.price_after_discount = price
            print("dito check >>>>>>>>xxxx>>>>>>", rec.price_after_discount)

    @api.onchange('price_after_discount')
    def _onchange_price_after_discount(self):
        for rec in self:
            if rec.price_after_discount:
                rec.price = rec.price_after_discount
            else:
                rec.price = 0

    # @api.onchange('product_pricelist_id')
    # def _onchange_product_pricelist_id(self):
    #     for rec in self:
    #         print('==============================================');
    #         print('==================== reza ====================');
    #         print('==================== rec.product_pricelist_id    ------------------>',rec.product_pricelist_id);
    #         print('==================== reza ====================');
    #         print('==============================================');
            
    #         if rec.product_pricelist_id:
    #             PricelistItem = self.env["product.pricelist.item"]
    #             item = PricelistItem.search([("product_tmpl_id","=",self.product_tmpl_id.id),("pricelist_id","=",self.product_pricelist_id.id)])
    #             if item:
    #                 self.sales_price_before = item.fixed_price
    #             else:
    #                 self.sales_price_before = 0
    #         else:
    #             self.sales_price_before = 0

    @api.depends('product_pricelist_id','sales_price')
    def _compute_sales_price_before(self):
        for rec in self:
            if rec.product_pricelist_id:
                PricelistItem = self.env["product.pricelist.item"]
                item = PricelistItem.search([("product_tmpl_id","=",rec.product_tmpl_id.id),("pricelist_id","=",rec.product_pricelist_id.id)])
                if item:
                    self.sales_price_before = item.fixed_price
                else:
                    self.sales_price_before = 0
            else:
                self.sales_price_before = 0

   
    @api.depends('margin_ho','margin_toko','price')
    def _compute_sales_price(self):
        for rec in self:
            if rec.margin_ho > 0 or rec.margin_toko > 0:
                after_margin_ho = rec.price + (rec.price * rec.margin_ho / 100)
                after_margin_toko = after_margin_ho + ( after_margin_ho * rec.margin_toko / 100)
                rec.sales_price = after_margin_toko
            else:
                rec.sales_price = 0

    def update_sales_pricelist(self):
        PricelistItem = self.env["product.pricelist.item"]

        if self.product_pricelist_id :
            if self.sales_price > 0:
                item = PricelistItem.search([("product_tmpl_id","=",self.product_tmpl_id.id),("pricelist_id","=",self.product_pricelist_id.id)])
                if item:
                    item.write({
                        "fixed_price" : self.sales_price
                    })
            else:
                item = PricelistItem.search([("product_tmpl_id","=",self.product_tmpl_id.id),("pricelist_id","=",self.product_pricelist_id.id)])
                if item:
                    item.write({
                        "fixed_price" : self.price
                    })
            
            self._compute_sales_price_before()

    # def action_view_form(self):
    #     for rec in self:
    #         obj = 'product.supplierinfo'
    #         vendor_ids = rec.env[obj].search([('product_tmpl_id', '=', rec.id)]).mapped('id')
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'view_mode' : 'form',
    #             'view_type' : 'form',
    #             'res_model' : obj,
    #             'view_id': self.env.ref('product.product_supplierinfo_form_view').id,
    #             'domain': [('id', 'in', vendor_ids)],
    #             'context': {'default_product_tmpl_id': rec.id},
    #             # 'target': 'main',
    #         }
    
    # @api.multi
    # def open_custom(self):
    #     view_id = self.env.ref('product.product_supplierinfo_form_view').id
    #     context = self._context.copy()
    #     return {
    #         'name': 'product_supplierinfo_tree_view_ksi_stock_kb',
    #         'view_type': 'form',
    #         'view_mode': 'tree',
    #         'views' : [(view_id,'form')],
    #         'res_model': 'product_supplierinfo',
    #         'view_id': view_id,
    #         'type': 'ir.actions.act_window',
    #         'res_id': self.id,
    #         'target': 'new',
    #         'context': context,
    #     }
    
    def open_view(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': rec._name,
                'view_id': self.env.ref('product.product_supplierinfo_form_view').id,
                'target': 'current',
                'res_id': rec.id,
            }
