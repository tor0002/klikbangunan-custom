from odoo import models, api
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _check_picking_done(self):
        """Helper method to check if the state is done."""
        if self.state != 'done':
            raise ValidationError("You cannot print the delivery slip as the state is not 'done'.")

    def action_report_delivery(self):
        """Override method to block printing delivery slip if state is not done."""
        self._check_picking_done()  # Call the validation method
        return super(StockPicking, self).action_report_delivery()

    def action_print(self):
        """Override generic print method for blocking printing."""
        self._check_picking_done()
        return super(StockPicking, self).action_print()

    def action_custom_print(self):
        """Override any other custom print action if applicable."""
        self._check_picking_done()
        return super(StockPicking, self).action_custom_print()
