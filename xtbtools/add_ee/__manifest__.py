# -*- coding: utf-8 -*-
{
    'name': 'Addenda Base EE',
    'version': '1.00',
    'category': 'Account',
    'author': 'xmartb',
    'website': 'http://www.xmartb.com',
	'license': 'OPL-1',
    'summary': 'Base para Addenda para timbrado XML',
    'description': """
Addendas:
========
* Modulo base
    """,
    'depends': [
        "account",
        "l10n_mx_edi",
        ],
    'data': [
        "views/invoice_view.xml",
         ],
    'js': [
        ],
    'installable': True,
    'application': True,
    'active': False
}
