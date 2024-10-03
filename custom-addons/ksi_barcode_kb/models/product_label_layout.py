# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, api, fields, models
from odoo.exceptions import UserError
from collections import defaultdict



class KSIProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    # ! Untuk pricelist_id
    def _get_default_pricelist(self):
        default_pricelist_id = self.env['product.pricelist'].search([])[2].id
        return default_pricelist_id

    print_format = fields.Selection(selection_add=[
    ('custom_kb', 'KlikBangunan'),
    ('custom_kbandprice', 'KlikBangunan with price'),
    ],ondelete={'custom_kb': 'set default', 'custom_kbandprice': 'set default'}, string="Format", default='custom_kbandprice', required=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Price List')
  
   
    # def _prepare_report_data(self):
    #     xml_id, data = super()._prepare_report_data()

       
    #     return xml_id, data

    # ! Overloading karna harus edit flow
    def _prepare_report_data(self):
        if self.custom_quantity <= 0:
            raise UserError(_('You need to set a positive quantity.'))

        # Get layout grid
        if self.print_format == 'dymo':
            xml_id = 'product.report_product_template_label_dymo'
        elif 'x' in self.print_format:
            xml_id = 'product.report_product_template_label'
        else:
            xml_id = ''

        active_model = ''
        if self.product_tmpl_ids:
            products = self.product_tmpl_ids.ids
            active_model = 'product.template'
        elif self.product_ids:
            products = self.product_ids.ids
            active_model = 'product.product'

        # Build data to pass to the report
        data = {
            'active_model': active_model,
            'quantity_by_product': {p: self.custom_quantity for p in products},
            'layout_wizard': self.id,
            'price_included': 'xprice' in self.print_format,
        }
        
        # ! Custom
        if 'custom_kb' in self.print_format:
                xml_id = 'ksi_barcode_kb.ksi_custom_barcode'

        data['pricelist_id'] = self.pricelist_id.id
        data['price_included'] = 'xprice' in self.print_format or 'custom_kbandprice' in self.print_format
        
        # ! Custom override dari stock
        if 'zpl' in self.print_format:
                xml_id = 'stock.label_product_product'

        if self.picking_quantity == 'picking' and self.move_line_ids:
            qties = defaultdict(int)
            custom_barcodes = defaultdict(list)
            uom_unit = self.env.ref('uom.product_uom_categ_unit', raise_if_not_found=False)
            
            for line in self.move_line_ids:
                # ! Hanya yg tipenya category unit dan uom category pcs aja
                # if line.product_uom_id.category_id == uom_unit or line.product_uom_id.category_id.name == "PCS":
                #     if (line.lot_id or line.lot_name) and int(line.qty_done):
                #         custom_barcodes[line.product_id.id].append((line.lot_id.name or line.lot_name, int(line.qty_done)))
                #         continue
                #     qties[line.product_id.id] += line.qty_done

                # ! print label all uom
                if (line.lot_id or line.lot_name) and int(line.qty_done):
                    custom_barcodes[line.product_id.id].append((line.lot_id.name or line.lot_name, int(line.qty_done)))
                    continue
                qties[line.product_id.id] += line.qty_done
                    
            # Pass only products with some quantity done to the report
            data['quantity_by_product'] = {p: int(q) for p, q in qties.items() if q}
            data['custom_barcodes'] = custom_barcodes
    
            

        return xml_id, data

