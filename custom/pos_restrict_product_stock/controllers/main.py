# -*- coding: utf-8 -*-

from odoo.http import request
from odoo.addons.bus.controllers.main import BusController


class PosOrderController(BusController):

    def _poll(self, dbname, channels, last, options):
        """Add the relevant channels to the BusController polling."""
        if options.get('stock.pos'):
            channels = list(channels)
            lock_channel = (
                request.db,
                'stock.pos',
                options.get('stock.pos')
            )
            channels.append(lock_channel)
        return super(PosOrderController, self)._poll(dbname, channels, last, options)
