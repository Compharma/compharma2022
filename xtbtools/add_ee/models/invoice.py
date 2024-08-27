# -*- encoding: utf-8 -*-
#    Coded by: joseg.osuna@gmail.com
##############################################################################
import base64
from odoo import _, api, fields, models, tools, registry


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_mx_edi_addenda = fields.Many2one('ir.ui.view',
                                          string='Addenda',
                                          compute='_compute_l10n_mx_edi_addenda',
                                          readonly=True,
                                          store=True
                                          )

    @api.depends('partner_id.l10n_mx_edi_addenda')
    def _compute_l10n_mx_edi_addenda(self):
        for invoice in self:
            addenda = invoice.partner_id.l10n_mx_edi_addenda or invoice.partner_id.commercial_partner_id.l10n_mx_edi_addenda
            invoice.l10n_mx_edi_addenda = addenda


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    # @api.model
    # def _l10n_mx_edi_cfdi_append_addenda(self, invoice, cfdi, addenda):
    #     return {}





