{
    'name': 'Custom Delivery Slip Print',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Custom button to print delivery slips from batch transfer',
    'depends': ['stock', 'stock_picking_batch'],
    'data': [
        'views/picking_batch_views.xml',
    ],
}
