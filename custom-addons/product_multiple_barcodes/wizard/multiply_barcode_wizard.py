# Copyright 2021 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MultiplyBarcodeWizard(models.TransientModel):
    _name = 'multiply.barcode.wizard'
    _description = 'Update Product Multiply Barcode Wizard'

    def default_barcode(self):
        model_name = self.env.context['active_model']
        if model_name == 'product.product':
            product = self.env['product.product'].browse(self.env.context['active_id'])
        if model_name == 'product.template':
            product = self.env['product.template'].browse(
                self.env.context['active_id']
            ).product_variant_id

        if product.barcode_and_seq:
            tampung = product.barcode_and_seq
            hasil = tampung

            return hasil
        else:
            raise UserError(_("Please insert Prefix merk or Product Category Barcode Sequence"))

    name = fields.Char(
        string='New Barcode',
        required=True,
        default=default_barcode
    )

    remember_previous_barcode = fields.Boolean(
        string='Remember previous barcode in "Additional Barcodes" field',
        default=True,
    )

    def update_barcode(self):
        model_name = self.env.context['active_model']
        if model_name == 'product.product':
            product = self.env['product.product'].browse(self.env.context['active_id'])
        if model_name == 'product.template':
            product = self.env['product.template'].browse(
                self.env.context['active_id']
            ).product_variant_id

        get_sequence = self.env['ir.sequence'].next_by_code('ksi.unique.barcode')
        BarcodeNomen = self.env['barcode.nomenclature']
        DefaultNomen = BarcodeNomen.search([('id','=',self.env.ref("barcodes.default_barcode_nomenclature").id)])
        new_barcode = self.name + get_sequence

        if self.remember_previous_barcode:
            barcode = product.barcode



            if barcode:

                # ! debug
                if product.merk_prefix:


                    product_barcode_multi = self.env['product.barcode.multi'].create({
                        'name': barcode,
                        'product_id': product.id,
                    })

                    DefaultNomen.write({
                        'rule_ids' : [
                            (0,0,{
                            'name' : 'duplicate ' + product.name,
                            'sequence' : 1,
                            'type' : 'alias',
                            'pattern' : product_barcode_multi.name,
                            'alias' : new_barcode,
                            'multi_barcode_id' : product_barcode_multi.id, 
                        })
                        ]
                    })

                    product.write({
                        'barcode': new_barcode,
                        'default_code': new_barcode,
                        'barcode_ids': [(4, product_barcode_multi.id)],
                    })


                        
                else:
                    raise UserError(_("Please insert Prefix merk or Product Category Barcode Sequence"))

            else:
                product.write({
                    'barcode': new_barcode,
                    'default_code': new_barcode,

            })

        else:
            product.barcode = new_barcode
            product.write({
                "barcode" : new_barcode
            })
            product.default_code = new_barcode
