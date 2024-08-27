# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
##############################################################################

from lxml import etree
from lxml.objectify import fromstring
import time
import base64
import logging
import unicodedata
from odoo.exceptions import Warning, UserError, ValidationError
from odoo import _, api, fields, models, tools, registry

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

class AccountMove(models.Model):
    _inherit = 'account.move'

    insabi_osuministro = fields.Char('No. Orden de suministro', readonly=True, states={'draft':[('readonly', False)], })
    insabi_oremision = fields.Char('Orden de remisión', readonly=True, states={'draft':[('readonly', False)], })
    insabi_clues = fields.Char('CLUES', readonly=True, states={'draft':[('readonly', False)], })
    insabi_contrato = fields.Char('Contrato', readonly=True, states={'draft':[('readonly', False)], })
    insabi_fecha_expedicion = fields.Date('Fecha expedición', readonly=True, states={'draft':[('readonly', False)], })
    insabi_fecha_entrega = fields.Date('Fecha entrega', readonly=True, states={'draft':[('readonly', False)], })
    insabi_fecha_recepcion = fields.Date('Fecha recepción', readonly=True, states={'draft':[('readonly', False)], })

    def _is_addenda_insabi(self):
        self.ensure_one()
        if self.l10n_mx_edi_addenda:
            return self.move_type == 'out_invoice' and self.l10n_mx_edi_addenda == self.env.ref('add_insabi_ee.l10n_mx_edi_addenda_insabi')
        return False


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'


    @api.model
    def _l10n_mx_edi_cfdi_append_addenda(self, invoice, cfdi, addenda):

        if not invoice._is_addenda_insabi():
            return super(AccountEdiFormat, self)._l10n_mx_edi_cfdi_append_addenda(invoice, cfdi, addenda)

        if not addenda:
            return cfdi

        addenda_values = {'record': invoice, 'cfdi': cfdi}
        data_addenda = self._get_addenda_insabi_data(invoice)
        if data_addenda.get('error'):
            invoice.message_post(
                body="Error al agregar addenda: {}".format(data_addenda.get('error')),
                subtype='account.mt_invoice_validated')
            return cfdi

        addenda_values.update(data_addenda=data_addenda)

        addenda = self.env['ir.qweb']._render(addenda.id, values=addenda_values).strip()
        if not addenda:
            return cfdi

        cfdi_node = fromstring(cfdi)
        addenda_node = fromstring(addenda)
        version = cfdi_node.get('Version')

        # Add a root node Addenda if not specified explicitly by the user.
        if addenda_node.tag != '{http://www.sat.gob.mx/cfd/%s}Addenda' % version[0]:
            node = etree.Element(etree.QName('http://www.sat.gob.mx/cfd/%s' % version[0], 'Addenda'))
            node.append(addenda_node)
            addenda_node = node

        cfdi_node.append(addenda_node)
        invoice.message_post(body=_('Addenda has been added in the CFDI with success'))
        return etree.tostring(cfdi_node, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    def _get_addenda_insabi_data(self, invoice):

        addenda = invoice.partner_id.l10n_mx_edi_addenda or invoice.partner_id.commercial_partner_id.l10n_mx_edi_addenda
        if not addenda:
            return {'error': 'No se ha definido una Clave de proveedor para Walmart. En pestaña Addenda de Cliente Walmart'}
        if not invoice.insabi_osuministro:
            return {'error': 'No se ha definido una Orden de suministro para la addenda INSABI. En pestaña Addenda de la factura'}

        data = {
            'NOS': invoice.insabi_osuministro,
            'OR': invoice.insabi_oremision,
            'CLUES': invoice.insabi_clues,
            'CONTRATO': invoice.insabi_contrato,
            'FEEX': invoice.insabi_fecha_expedicion.strftime("%d/%m/%Y"),
            'FEEN': invoice.insabi_fecha_entrega.strftime("%d/%m/%Y"),
            'FERE': invoice.insabi_fecha_recepcion.strftime("%d/%m/%Y"),
        }

        data_addenda = {
            'insabi_data': data,
        }

        return data_addenda
