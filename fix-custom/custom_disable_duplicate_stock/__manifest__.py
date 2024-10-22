{
    'name': 'Disable Duplicate Vendor Reference Check',
    'description': 'Modul ini berisi 2 custom yaitu mengdisable duplicate vendor (bisa melakukan validate receipt lebih dari 2 kali dalam 1 hari, menambahkan button untuk link dari PO dan SO)',
    'depends': ['account','purchase', 'sale'],
    'data': [
        'views/purchase_order_views.xml'
        ],
    'installable': True,
    'applicable': True,
}
