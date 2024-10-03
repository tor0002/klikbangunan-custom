# Copyright 2021 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    multi_barcode_id = fields.Many2one('product.barcode.multi', string='Multi Barcode', ondelete="cascade")
    