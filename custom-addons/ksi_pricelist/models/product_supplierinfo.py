from odoo import _, api, fields, models

class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'
    _description = 'Product Supplierinfo'
    
    new_cost_price = fields.Float('New Cost Price', tracking=True)
    current_sale_price = fields.Float('Sale Price', related='product_tmpl_id.list_price')
    new_sale_price = fields.Float('New Sale Price', tracking=True)

   
    def change_vendor_prices(self):
        for rec in self:
            rec.write({
                'price' : rec.new_cost_price
            }) 

       
    def change_sales_prices(self):
        for rec in self:
            rec.product_tmpl_id.write({
                'list_price' : rec.new_sale_price
            })
        