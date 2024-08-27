# -*- coding: utf-8 -*-
{
    'name': 'Addenda INSABI EE',
    'version': '1.00',
    'category': 'Account',
    'author': 'xmartb',
    'website': 'http://www.xmartb.com',
	'license': 'OPL-1',
    'summary': 'Addenda INSABI CFDI',
    'description': """
Addendas:
========
* INSABI
    """,
    'depends': [
        "account",
        "product",
        "l10n_mx_edi",
        "l10n_mx_edi_40",
        "l10n_mx_edi_extended",
        "l10n_mx_edi_extended_40",
        "add_ee",
        ],
    'data': [
        "templates/addenda_insabi_view.xml",
        "views/insabi_view.xml",
         ],
    'js': [
        ],
    'installable': True,
    'application': True,
    'active': False
}
