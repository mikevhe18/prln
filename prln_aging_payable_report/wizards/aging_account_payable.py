# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Michael Viriyananda
#    Copyright 2015 OpenSynergy Indonesia
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _


class aging_account_payable(osv.osv_memory):
    _name = 'pralon.aging_account_payable'
    _description = 'Daftar Aging Account Payable'

    _columns = {
        'company_ids': fields.many2many(
            obj='res.company',
            rel='aging_acc_payable_company_rel',
            id1='wizard_id',
            id2='company_id',
            string='Companies'
        ),
        'supplier_ids': fields.many2many(
            obj='res.partner',
            rel='aging_acc_payable_supplier_rel',
            id1='wizard_id',
            id2='supplier_id',
            string='Supplier'
        ),
        'invoice_date_from': fields.date(
            string='Invoice Date From',
            required=False
        ),
        'invoice_date_to': fields.date(
            string='Invoice Date To',
            required=False
        ),
        'date_as_of': fields.date(
            string='Date As Of',
            required=True
        ),
        'output_format': fields.selection(
            string='Output Format',
            required=True,
            selection=[('pdf', 'PDF'), ('xls', 'XLS')])
    }

    def fields_view_get(
        self, cr, uid, view_id=None, view_type='form',
        context=None, toolbar=False, submenu=False
    ):
        res = super(aging_account_payable, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type,
            context=context, toolbar=toolbar, submenu=False)

        if view_type == 'form':

            for field in res['fields']:
                if field == 'supplier_ids':
                    res['fields'][field]['domain'] = [('supplier', '=', 1)]
        return res

    def button_print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        output_format = ''

        if context is None:
            context = {}

        datas['form'] = self.read(cr, uid, ids)[0]

        invoice_date_from = datas['form']['invoice_date_from']
        invoice_date_to = datas['form']['invoice_date_to']

        if invoice_date_from > invoice_date_to:
            err = 'Invoice Date From cannot be greater than Invoice Date To'
            raise osv.except_osv(_('Warning'), _(err))

        if datas['form']['output_format'] == 'xls':
            output_format = 'report_aging_account_payable_xls'
        elif datas['form']['output_format'] == 'pdf':
            output_format = 'report_aging_account_payable_pdf'
        else:
            err = 'Output Format cannot be empty'
            raise osv.except_osv(_('Warning'), _(err))

        return {
            'type': 'ir.actions.report.xml',
            'report_name': output_format,
            'datas': datas,
        }

aging_account_payable()
