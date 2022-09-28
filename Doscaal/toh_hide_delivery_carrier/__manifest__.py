# -*- coding: utf-8 -*-
{
    'name': "Ocultar transportista de entrega en metodo de envio",

    'summary': """
        Ocultar transportista de entrega en método de envío.
        Hide delivery carrier""",

    'description': """
        Oculta el método de envío de acuerdo a la clasificación B2B o B2C del cliente.
        Hide the shipping method according to the customer's B2B or B2C classification
    """,

    'author': "Toh Soluciones Digitales",
    'website': "http://www.tohsoluciones.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management','delivery'],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
        'views/delivery_carrier_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'images': ["static/description/b2c_ecommerce.jpg"],
    'license': "AGPL-3",
}
