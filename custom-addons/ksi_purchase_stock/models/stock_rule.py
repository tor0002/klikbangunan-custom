from odoo import _, api, fields, models

class StockRule(models.Model):
    _inherit = 'stock.rule'
    _description = 'Stock Rule'
    
    # ! remove date domain, po will merge if vendor and picking_type_id is same and still in draft
    def _make_po_get_domain(self, company_id, values, partner):
        domain = super(StockRule, self)._make_po_get_domain(company_id, values, partner)
        if values.get('orderpoint_id'):
            list_domain = [t for t in domain if t[0] != 'date_order']
            domain = tuple(list_domain)
                
        return domain
        