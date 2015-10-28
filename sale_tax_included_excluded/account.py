# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale Tax Included Excluded module for Odoo
#    Copyright (C) 2014-2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    price_include_taxes = fields.Boolean('Price Include Taxes')

    @api.multi
    @api.constrains('price_include_taxes', 'tax_ids')
    def _check_price_include_taxes(self):
        for fp in self:
            for tax_pos in fp.tax_ids:
                if (
                        tax_pos.tax_dest_id and
                        tax_pos.tax_dest_id.amount and
                        fp.price_include_taxes !=
                        tax_pos.tax_dest_id.price_include):
                    raise ValidationError(
                        _("The fiscal position '%s' %s 'Price Include Taxes' "
                            "but it has a "
                            "replacement tax '%s' which has a non-null "
                            "amount and %s 'Tax Included in Price'.")
                        % (fp.name,
                            fp.price_include_taxes and _('is') or _('is not'),
                            tax_pos.tax_dest_id.name,
                            tax_pos.tax_dest_id.price_include and
                            _('is') or _('is not')))


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def _fix_tax_included_price(self, cr, uid, price, prod_taxes, line_taxes):
        '''This module is incompatible with this new method introduced
        in Odoo v8 on August 24th 2015. So I inherit this method to
        return the same price as input'''
        print "_fix_tax_included_price====", price
        return price
