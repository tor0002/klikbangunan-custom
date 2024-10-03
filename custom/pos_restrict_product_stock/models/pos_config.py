# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Gayathri V(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import fields, models


class PosConfig(models.Model):
    """Inherited pos configuration setting for adding some
            fields for restricting out-of stock"""
    _inherit = 'pos.config'

    is_display_stock = fields.Boolean(string="Display Stock in POS",
                                      help="Enable if you want to show "
                                           "quantity of products")
    # is_restrict_product = fields.Boolean(
    #     string="Restrict Product Out-of Stock in POS",
    #     help="Enable if you want restrict of stock product from pos")
    
    stock_type = fields.Selection([('qty_on_hand', 'Qty on Hand'),
                                   ('virtual_qty', 'Virtual Qty')], required=True,
                                  default='qty_on_hand', string="Stock Type",
                                  help="In which quantity type you"
                                       " have to restrict and display")
    

    def get_product_qty(self):
        self.ensure_one()
        products = self.env['product.product'].search([('available_in_pos', '=', True)])
        result = []
        for product in products:
            q = 0
            if self.stock_type == 'qty_on_hand':
                q = product.qty_available
            if self.stock_type == 'virtual_qty':
                q = product.virtual_available
            result.append({'id': product.id, 'quantity': q})
        return result