# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError

# ! Copy from default
def _prepare_data(env, data):
    # !Custom, kita bikin template data sendiri
    data_label_barcode = []
    
    if data.get('active_model') == 'product.template':
        produk_apa = 'product_template'
    elif data.get('active_model') == 'product.product':
        produk_apa = 'product_product'
    else:
        raise UserError(_('Product model not defined, Please contact your administrator.'))

    for p, q in data.get('quantity_by_product').items():
        # product = Product.browse(int(p))
        # ! Hanya print yg ada barcodenya aja
        if produk_apa == "product_template":
            sql = """
                select id,name,default_code,list_price
                from product_template
                where id=%s
            """
            cr = env.cr
            cr.execute(sql, (int(p),))
            res_sql_product = cr.fetchone()

        # ! Kalo dia product_product, balikin jadi product_tempalate
        if produk_apa == "product_product":
            sql = """
                select product_tmpl_id
                from product_product
                where id=%s
            """
            cr = env.cr
            cr.execute(sql, (int(p),))
            res_sql_product_tmpl_id = cr.fetchone()
         

            sql = """
                select id,name,default_code,list_price
                from product_template
                where id=%s
            """
            cr = env.cr
            cr.execute(sql, (int(res_sql_product_tmpl_id[0]),))
            res_sql_product = cr.fetchone()
       
        if res_sql_product:
            if data.get('pricelist_id'):
                # ! Obat kuat
                sql = """
                    select fixed_price
                    from product_pricelist_item
                    where product_tmpl_id=%s AND pricelist_id=%s
                """
                cr = env.cr
                cr.execute(sql, (res_sql_product[0],data.get('pricelist_id'),))
                res_sql = cr.fetchone()
                
                
                # ! Kalo Pake Priclsit
                data_label_barcode += ([[res_sql_product[1],res_sql_product[2], float(res_sql[0])]] * q)


            else:
                # ! Kalo pake sales price
                data_label_barcode += ([[res_sql_product[1],res_sql_product[2], res_sql_product[3]]] * q)
            

    # ! Kelompokkan jadi masing2 3 lebel
    def list_split(listA, n):
        for x in range(0, len(listA), n):
            every_chunk = listA[x: n+x]

            if len(every_chunk) < n:
                every_chunk = every_chunk + \
                    [None for y in range(n-len(every_chunk))]
            yield every_chunk
    data_label_row = list(list_split(data_label_barcode, 3))
    

    # raise UserError(_("Stop, liat log"))

    return {
        'price_included': data.get('price_included'),
        'data_label_row' : data_label_row
    }

class KSIReportProductTemplateLabelDymo(models.AbstractModel):
    _name = 'report.ksi_barcode_kb.ksi_custom_layout_barcode'
    _description = 'Product Label Report'

    def _get_report_values(self, docids, data):
        
        return _prepare_data(self.env, data)
