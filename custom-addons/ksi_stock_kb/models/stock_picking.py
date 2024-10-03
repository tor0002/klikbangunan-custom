from odoo import _,api,models,fields
from lxml import etree
from odoo.exceptions import ValidationError
import json

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking (inherited by ksi_stock_kb)'
    
    nama_supir = fields.Char('Nama Supir')
    nopol_kendaraan = fields.Char('No. Pol. Kendaraan')
    
    from_purchase = fields.Boolean(string='Purchase', related='purchase_id.from_purchase',store=True)
    from_sale = fields.Boolean(string='Sale', related='sale_id.from_sale',store=True)

    active = fields.Boolean(string='Active', default=True)

    def _check_qty_done(self):
        for rec in self:
            # print('dito >>>>>>>>>>>>XXXX>>>>',self)
            for line in rec.move_ids_without_package:
                # print('dito >>>>>>>>>>>>XXXX>>>>',line)
                if line.quantity_done > line.product_uom_qty:
                    # print('dito >>>>>>>>>>>>XXXX>>>>',line.quantity_done)
                    # print('dito >>>>>>>>>>>>XXXX>>>>',line.product_uom_qty)
                    raise ValidationError("Quantity Done cannot be higher than Quantity")
    
    def _create_inv_and_bill_from_warehouse(self, inv=False):
        for rec in self:
            # melihat config
            auto_validate_post_invoice = self.env['ir.config_parameter'].sudo().get_param('automatic_invoice_and_post.is_create_post_invoice_delivery_validate')
            auto_validate_invoice = self.env['ir.config_parameter'].sudo().get_param('automatic_invoice_and_post.is_create_invoice_delivery_validate')
            
            # auto create bill
            if auto_validate_invoice and rec.picking_type_id.code == 'incoming':
                purchase_order = self.env['purchase.order'].search([('name', '=', rec.origin)])
                if purchase_order:
                    bill_created = purchase_order.action_create_bill()
                    # print("dito >>>>",bill_created)
                    if auto_validate_post_invoice and bill_created:
                        bill_created.invoice_date = fields.Date.today()
                        # print("dito>>>>>",bill_created.invoice_date)
                        bill_created.action_post()
            
            # auto create inv
            if auto_validate_invoice and rec.picking_type_id.code == 'outgoing':
                sale_order = self.env['sale.order'].search([('name', '=', rec.origin)], limit=1)
                if sale_order:
                    invoice_created = sale_order._create_invoices(inv_do=inv)
                    if auto_validate_post_invoice and invoice_created:
                        invoice_created.action_post()

                # if any(rec.product_id.invoice_policy == 'delivery' for rec in self.move_ids_without_package) or not self.sale_id.invoice_ids:
                    # print('dito >>>>>>>>>>>>XXXX>>>>')
                    # Call the _create_invoices function on the associated sale
                    # to create the invoice
                    # invoice_created = self.sale_id._create_invoices(self.sale_id) if self.sale_id else False
                        # invoice_created = sale_order._create_invoices()

    

    def button_validate(self):
        # self._check_qty_done()
        # self._create_inv_and_bill_from_warehouse()
        validate = super(StockPicking, self).button_validate()
        if not self._check_backorder():
            self._create_inv_and_bill_from_warehouse()
        return validate
        
    # @api.model
    # def fields_view_get(self, view_id=None, view_type="tree,form", toolbar=False, submenu=False):
    #     result = super(StockPicking, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     doc = etree.XML(result["arch"])
    #     if view_type == "tree" or view_type == "form":
    #         for form in doc.xpath("//page[@name='operations']/field/tree"):
    #             if self.from_purchase:
    #                 form.set("create", "True")
    #                 # form.set("delete", "false")
    #                 # form.set("edit", "false")
    #     result["arch"] = etree.tostring(doc, encoding="unicode")
    #     return result

    # not_from_sale = fields.Boolean(compute='_compute_not_from_sale', string='Is not from Sale?')
    
    # @api.depends('sale_id')
    # def _compute_not_from_sale(self):
    #     for me in self:
    #         print("SALEEEEE", me.sale_id)
    #         me.not_from_sale = False
    #         if not me.sale_id:
    #             me.not_from_sale = True
    
    # not_from_purchase = fields.Boolean(compute='_compute_not_from_purchase', string='Is not from Purchase?')
    
    # @api.depends('purchase_id')
    # def _compute_not_from_purchase(self):
    #     for me in self:
    #         print("PURCHASE", me.purchase_id)
    #         me.not_from_purchase = False
    #         if not me.purchase_id:
    #             me.not_from_purchase = True

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form',
    #                     toolbar=False, submenu=False):
    #     res = super(StockPicking, self).fields_view_get(
    #         view_id=view_id, view_type=view_type,
    #         toolbar=toolbar, submenu=submenu)
    #     print('==============================================');
    #     print('==================== reza ====================');
    #     print('==================== masuk field_view_get    ------------------>');
    #     print('==================== reza ====================');
    #     print('==============================================');
        
    #     # Check if user is in group that allow creation
    #     if self.purchase_id or self.sale_id:
    #         print('==============================================');
    #         print('==================== reza ====================');
    #         print('==================== masuk if fvg    ------------------>');
    #         print('==================== reza ====================');
    #         print('==============================================');
            
    #         root = etree.fromstring(res['arch'])
    #         print('==============================================');
    #         print('==================== reza ====================');
    #         print('==================== root    ------------------>',root);
    #         print('==================== reza ====================');
    #         print('==============================================');
            
    #         root.set('create', 'false')
    #         res['arch'] = etree.tostring(root)

    #     return res
    
    @api.model

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        res = super().fields_view_get(

            view_id=view_id,

            view_type=view_type,

            toolbar=toolbar,

            submenu=submenu)
        
        # print("GET RES YO!", json.dumps(res, indent=1))
        
        # if res.get('fields').get('state')['selection'][0][1] == 'assigned':

        #     if res.get('toolbar', False) and res.get('toolbar').get('print', False):

        #         reports = res.get('toolbar').get('print')

        #         for report in reports:

        #             if report.get('report_file', False) and report.get('report_file') == 'stock.report_deliveryslip':

        #                 res['toolbar']['print'].remove(report)
        
        # return res
        
        context = self._context or {}
        # print("CONTEXT", context)
        
        if len(context) > 0:
            # get_state = self.env['stock.picking'].search([('id', '=', context['params']['id'])])
            # print("GET STATE", get_state)
            
            # active_id = self.env['stock.picking'].browse(context['active_id'])
            # print("ACTIVE ID", active_id)
            
            remove_report_ids = []
            remove_report_ids.append(self.env.ref('stock.report_picking').id)
            remove_report_ids.append(self.env.ref('stock.report_deliveryslip').id)
            print("GET REPORTS TO REMOVE", remove_report_ids)
            # print("GET FIELDS", res['fields'].get('state'))
            
            if view_type == 'form' and remove_report_ids and toolbar and res['toolbar'] and res['toolbar'].get('print'):
                print("TOOLBAR >>> PRINT", res['toolbar'].get('print'))
                remove_report_ids = [339, 340]
                remove_report_records = [rec for rec in res['toolbar'].get('print') if rec.get('id') in remove_report_ids]
                print("remove_report_records", remove_report_records)
                
                # doc = etree.XML(res['arch'])
                # The field you want to modify the attribute
                # node = doc.xpath("//field[@name='state']")[0]
                # print("NODE", node.get('key'))
                
                for rec in remove_report_records:
                    # if rec and rec[0]:
                    # print("MULAI HAPUS")
                    res['toolbar'].get('print').remove(rec)
        
        return res


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'
    _description = 'Purchase Order Inherit KSI'

    picking_line = fields.One2many('stock.picking', 'purchase_id', string='Purchase')
    move_line = fields.One2many('stock.move', 'purchase_id', string='Purchase')
    from_purchase = fields.Boolean(string='Purchase',store=True)

    def button_confirm(self):
        res =super(PurchaseOrderInherit, self).button_confirm()
        self.from_purchase = True

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order Inherit KS'

    picking_line = fields.One2many('stock.picking', 'purchase_id', string='Purchase')
    move_line = fields.One2many('stock.move', 'purchase_id', string='Purchase')
    from_sale = fields.Boolean(string='Sale',store=True)

    def action_confirm(self):
        res =super(SaleOrderInherit, self).action_confirm()
        self.from_sale = True
    

class StockMoveInherit(models.Model):
    _inherit = 'stock.move'
    _description = 'Stock Move'

    purchase_id = fields.Many2one('purchase.order', string='purchase')
    from_purchase = fields.Boolean(string='Purchase', related='purchase_id.from_purchase',store=True)
    sale_id = fields.Many2one('sale.order', string='sale')
    from_sale = fields.Boolean(string='Sale', related='sale_id.from_sale',store=True)
    # dipindah ke modul baru
    # custom_customer_note = fields.Char('Cstomer Note', compute='_compute_custom_customer_note',store=True)
    # custom_weight = fields.Float('Weight', related='product_id.weight')
    # total_weight = fields.Float('Total Weight', compute='_compute_custom_weight')

    # @api.depends('picking_id.origin')
    # def _compute_custom_customer_note(self):
    #     # self.custom_customer_note = self.picking_id.name
    #     for move in self:
    #         move.custom_customer_note = '' #perlu diperhatikan lesson dr lord aul
    #         print('dito test>>>>>>>>>>>>>>',move.picking_id.name)
    #         if move.picking_id and move.picking_id.origin:
    #             pos_order = self.env['pos.order'].search([('name', '=', move.picking_id.origin)])
    #             if pos_order:
    #                 pos_order_line = pos_order.lines.filtered(
    #                     lambda line: line.product_id == move.product_id
    #                 )
    #                 if pos_order_line:
    #                     move.custom_customer_note = pos_order_line.customer_note

    # @api.onchange('product_id')
    # def _onchange_weight(self):
    #     self.custom_weight = self.product_id.weight
    #     if self.product_uom_qty:
    #         self.total_weight = self.custom_weight * self.product_uom_qty
    
    # @api.depends('custom_weight','quantity_done')
    # def _compute_custom_weight(self):
    #     for line in self:
    #         line.total_weight = line.custom_weight * line.quantity_done