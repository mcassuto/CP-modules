# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Marc Cassuto <marc.cassuto@gmail.com>.
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

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class ProductPricelistItem(osv.osv):
    _inherit = "product.pricelist.item"

    def _get_prices(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        if context is None:
            context = {}

        currency_obj = self.pool.get('res.currency')
        product_obj = self.pool.get('product.product')
        product_uom_obj = self.pool.get('product.uom')
        price_type_obj = self.pool.get('product.price.type')

        for pvi in self.browse(cr, uid, ids, context=context):
            res[pvi.id] = {}

            product_id = pvi.product_id
            pricelist_currency_id = \
                pvi.price_version_id.pricelist_id.currency_id.id

            # COMPUTE list_price
            # price_type = 'list_price' => parameter = 1
            price_type = price_type_obj.browse(cr, uid, 1)
            price = currency_obj.compute(
                cr, uid,
                price_type.currency_id.id,
                pricelist_currency_id,
                product_obj.price_get(cr, uid,
                                      [product_id.id],
                                      'list_price',
                                      context=context
                                      )[product_id.id],
                round=False,
                context=context)
            res[pvi.id]['list_price'] = price

            # COMPUTE standard_price
            # price_type = 'standard_price' => parameter = 2
            price_type = price_type_obj.browse(cr, uid, 2)
            price = currency_obj.compute(
                cr, uid,
                price_type.currency_id.id,
                pricelist_currency_id,
                product_obj.price_get(cr, uid,
                                      [product_id.id],
                                      'standard_price',
                                      context=context
                                      )[product_id.id],
                round=False,
                context=context)
            res[pvi.id]['standard_price'] = price

            # COMPUTE computed_price
            # Pricelist version item based on another pricelist
            if pvi.base == -1:
                price = False
            # Pricelist version item based on Supplier price on the product
            # form
            elif pvi.base == -2:
                price = False
            # Pricelist version item based on any other pricetype
            else:
                price_type = price_type_obj.browse(cr, uid, int(pvi.base))
                price = currency_obj.compute(
                    cr, uid,
                    price_type.currency_id.id,
                    pricelist_currency_id,
                    product_obj.price_get(cr, uid,
                                          [product_id.id],
                                          price_type.field,
                                          context=context
                                          )[product_id.id],
                    round=False,
                    context=context)

                if price is not False:
                    price_limit = price
                    price *= (1.0 + pvi.price_discount or 0.0)
                    if pvi.price_round:
                        price = tools.float_round(
                            price,
                            precision_rounding=pvi.price_round
                        )
                    if context.get('uom'):
                        # compute price_surcharge based on reference uom
                        factor = product_uom_obj.browse(
                            cr, uid,
                            context.get('uom'),
                            context=context
                        ).factor
                    else:
                        factor = 1.0
                    price += (pvi.price_surcharge or 0.0) / factor
                    if pvi.price_min_margin:
                        price = max(price, price_limit + pvi.price_min_margin)
                    if pvi.price_max_margin:
                        price = min(price, price_limit + pvi.price_max_margin)

            res[pvi.id]['computed_price'] = price

            # COMPUTE margin (Computed Price - Cost) * 100 / Cost
            res[pvi.id]['margin'] = \
                res[pvi.id]['standard_price'] and \
                (res[pvi.id]['computed_price'] -
                 res[pvi.id]['standard_price']
                 ) * 100 / res[pvi.id]['standard_price']
        return res

    _columns = {
        'list_price': fields.function(
            _get_prices,
            multi='prices',
            type='float',
            digits_compute=dp.get_precision('Product Price'),
            string=_('Default sale price'),
            readonly=True),
        'standard_price': fields.function(
            _get_prices,
            multi='prices',
            type='float',
            digits_compute=dp.get_precision('Product Price'),
            string=_('Cost'),
            readonly=True),
        'computed_price': fields.function(
            _get_prices,
            multi='prices',
            type='float',
            digits_compute=dp.get_precision('Product Price'),
            string=_('Computed Price'),
            help=_('Computed price for the related product in this rule')),
        'margin': fields.function(
            _get_prices,
            multi='prices',
            type='float',
            string=_('Margin (%)'),
            help=_('(Computed Price - Cost) * 100 / Cost')),
    }
