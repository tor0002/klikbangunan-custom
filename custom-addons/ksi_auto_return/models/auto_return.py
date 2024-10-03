# from odoo import _, api, fields, models

# class AccountMove(models.Model):
#     _inherit = 'account.move'

    # dito = fields.Char('Dito')
    
    # @api.model
    # def auto_return(self):
        
    #     # print('dito check env>>>>>>>',self.env[stock.picking].search(["origin","=","return"]))
    #     debit_data = self.env['stock.picking'].search(["origin", "=", "return"])
    #     print('dito check env>>>>>>>>>>>',debit_data)
    #     return 0
    # @api.model
    # def create_from_picking(self):
    #     picking_data = self.env['stock.picking'].search([('origin', '=', 'return')])
    #     for picking in picking_data:
    #         partner_id = picking.partner_id.id
    #         for move_line in picking.move_lines:
    #             product_id = move_line.product_id.id
    #             move_vals = {
    #                 'partner_id': partner_id,
    #                 'product_id': product_id,
    #                 # Add other fields as needed
    #             }
    #             self.env['account.move'].create(move_vals)

# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
    
#     dito = fields.Char('Dito')

#     def button_validate(self):
#         print("dito check>>>>>>>>>>>>>>>>>>>")
#         self.env['account.move'].create({'ref': 'dito'})
#         res = super(StockPicking, self).button_validate()
        
#         return res

#     def auto_return(self):
#         print("dito check>>>>>>>>>>>>>>>>>>>")
#         return self.env['account.move'].create({'ref': 'dito','payment_reference':'dito2'})
        # refunds = []
        # refunds_list = []
        # component = self.move_ids_without_package
        # print("dito check>>>>>>>>>>>>>>>>>>>", component)
        # for rec in component :
        #     refunds_list.append(rec)

        #     stock_line = {
        #         'product_id': rec.product_id.name,
        #     }
        #     print('dito check>>>>>>>>>>>>>>>>>>',stock_line)

        #     refunds.append((0, 0, stock_line))
        
        # if refunds:
        #     vals = {
        #         'partner_id': self.partner_id.name,
        #         # 'picking_type_id': picking_type.id,
        #         # ! dari mr
        #         # 'origin': self.name,
        #         # 'move_type': 'direct',
        #         # 'location_dest_id': get_dest_loc if get_dest_loc > 0 else location_id,
        #         # 'location_id': prop_stock_sup.id if len(prop_stock_sup) > 0 else location_dest_id,
        #         # 'company_id': self.env.company.id,
        #         # 'user_id': self.env.user.id,
        #         # 'move_ids_without_package': component_opr,
        #         # 'order_number': self.analytic_account_id.name,
        #     }

        #     create_picking = self.env['account.move'].create(vals)

        # return True
