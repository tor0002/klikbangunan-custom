# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError

def _prepare_data(env, data):
    # change product ids by actual product object to get access to fields in xml template
    # we needed to pass ids because reports only accepts native python types (int, float, strings, ...)

    if data.get('active_model') == 'product.template':
        Product = env['product.template'].with_context(display_default_code=False)
    elif data.get('active_model') == 'product.product':
        Product = env['product.product'].with_context(display_default_code=False)
    else:
        raise UserError(_('Product model not defined, Please contact your administrator.'))


    total = 0
    quantity_by_product = defaultdict(list)
    for p, q in data.get('quantity_by_product').items():
        product = Product.browse(int(p))

        # ! Kondisi ke pricelist
        # ['|', ('product_tmpl_id', '=', template.id), ('product_id', 'in', template.product_variant_ids.ids)]
        price_from_pricelist = 0
        # ! Nambahin harga pricelist
        # ! This maybe need obat kuat aka SQL
        if data.get('pricelist_id'):
            print('==============================================');
            print('==================== reza ====================');
            print('==================== data.get('')    ------------------>',data.get('pricelist_id'));
            print('==================== reza ====================');
            print('==============================================');
            
            pricelist_item = env['product.pricelist.item'].search([("product_tmpl_id","=",product.id),("pricelist_id","=",data.get('pricelist_id'))])
        # else:
        #     raise UserError(_('Please insert the pricelist'))

            price_from_pricelist = pricelist_item.fixed_price
            
        print('==============================================');
        print('==================== reza ====================');
        print('==================== price_from_pricelist berapa ------------------>',price_from_pricelist);
        print('==================== reza ====================');
        print('==============================================');
        
        quantity_by_product[product].append((product.barcode, q, price_from_pricelist))
        total += q
    if data.get('custom_barcodes'):
        # we expect custom barcodes format as: {product: [(barcode, qty_of_barcode)]}
        for product, barcodes_qtys in data.get('custom_barcodes').items():
            quantity_by_product[Product.browse(int(product))] += (barcodes_qtys)
            total += sum(qty for _, qty in barcodes_qtys)

    layout_wizard = env['product.label.layout'].browse(data.get('layout_wizard'))
    if not layout_wizard:
        return {}


    
    return {
        'quantity': quantity_by_product,
        'rows': layout_wizard.rows,
        'columns': layout_wizard.columns,
        'page_numbers': (total - 1) // (layout_wizard.rows * layout_wizard.columns) + 1,
        'price_included': data.get('price_included'),
        'extra_html': layout_wizard.extra_html,
    }

class KSIInheritProductLabel(models.AbstractModel):
    _inherit = 'report.product.report_producttemplatelabel'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)
    
