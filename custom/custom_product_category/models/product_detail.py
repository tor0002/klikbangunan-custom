from odoo import fields, models

class Divisi(models.Model):
    _name = 'divisi'
    _rec_name = 'x_divisi_name'
    
    x_divisi_name = fields.Char(string='Divisi', required=True)
    
class Department(models.Model):
    _name = 'department'
    _rec_name = 'x_department_name'
    
    x_department_name = fields.Char(string='Department', required=True)
    
# class Category(models.Model):
#     _name = 'category'
#     _rec_name = 'x_category_name'  
    
#     x_category_name = fields.Char(string='Category', required=True)
    
# class Subcat(models.Model):
#     _name = 'subcat'
#     _rec_name = 'x_subcat_name'
    
#     x_subcat_name = fields.Char(string='Subcategory', required=True)