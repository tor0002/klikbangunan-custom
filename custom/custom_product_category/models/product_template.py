from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    x_divisi_name = fields.Many2one('divisi', string='Divisi', required=True)
    x_department_name = fields.Many2one('department', string='Department', required=True)
    # x_category_name = fields.Many2one('category', string='Category', required=True)
    # x_subcat_name = fields.Many2one('subcat', string='Subcategory', required=True)