# copyright Doscaal 2022
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# -*- coding: utf-8 -*-

{
    'name': 'Alodis Profile',
    'version': '18.0.1.0',
    'category': 'Custom',
    'description': """Profile for Alodis""",
    'author': 'Doscaal',
    'website': 'http://www.doscaal.fr/',
    'depends': [
        'base',
        'sale_loyalty',
        'sale_management',
    ],
    'images': [],
    'data': [
        'views/loyalty_card.xml',
        'views/loyalty_program.xml',
    ],
    'qweb': [],
    'test': [],
    'installable': True,
    'active': True,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
