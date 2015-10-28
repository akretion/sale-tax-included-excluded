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

from openerp import models, fields, api


class ProductPriceList(models.TransientModel):
    _inherit = 'product.price_list'

    pricelist_type = fields.Selection(
        related='price_list.type', string='Pricelist Type')
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', 'Fiscal Position')

    @api.multi
    def print_report(self):
        self.ensure_one()
        if self.pricelist_type == 'sale' and self.fiscal_position_id:
            rec = self.with_context(
                fiscal_position_id=self.fiscal_position_id.id)
            return super(ProductPriceList, rec).print_report()
        else:
            return super(ProductPriceList, self).print_report()
