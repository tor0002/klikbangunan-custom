from odoo import _,api,models,fields
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime

class StockInventoryAdjustmentName(models.TransientModel):
    _inherit = 'stock.inventory.adjustment.name'
    _description = 'Inventory Adjustment Reference / Reason (inherited by ksi_adjustment_kb)'
    
    def _default_inventory_adjustment_name(self):
        # res = super()._default_inventory_adjustment_name()
        # print("RES >>>>>>>", res)
        
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        current_time = now.strftime("%H:%M:%S")
        
        # print(">>>>>>> TIMESTAMP _default_inventory_adjustment_name", fields.datetime.now())
        return _("Inventory Adjustment") + " - " + str(current_date) + " - " + str(current_time)
    
    inventory_adjustment_name = fields.Char(default=_default_inventory_adjustment_name)
    
    def action_apply(self):
        if self.show_info:
            raise ValidationError("PERHATIAN: Ada kuantitas yang masih kosong!")
        else:
            res = super().action_apply()
            return res
