# -*- coding: utf-8 -*-
##############################################################################
#
#    @package lts_product_margin Bluecom Product for Odoo 8.0
#    @copyright Copyright (C) 2016 sy.luong@bluecom.vn. All rights reserved.#
#    @license http://www.gnu.org/licenses GNU Affero General Public License version 3 or later; see LICENSE.txt
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
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class purchase_order_line(osv.osv):
	_inherit = "purchase.order.line"
    # def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
    #         uom=False, qty_uos=0, uos=False, name='', partner_id=False,
    #         lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
    #     res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
    #         uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
    #         lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
    #     if not pricelist:
    #         return res
    #     if context is None:
    #         context = {}
    #     frm_cur = self.pool.get('res.users').browse(cr, uid, uid).company_id.currency_id.id
    #     to_cur = self.pool.get('product.pricelist').browse(cr, uid, [pricelist])[0].currency_id.id
    #     if product:
    #         product = self.pool['product.product'].browse(cr, uid, product, context=context)
    #         purchase_price = product.standard_price
    #         to_uom = res.get('product_uom', uom)
    #         if to_uom != product.uom_id.id:
    #             purchase_price = self.pool['product.uom']._compute_price(cr, uid, product.uom_id.id, purchase_price, to_uom)
    #         ctx = context.copy()
    #         ctx['date'] = date_order
    #         price = self.pool.get('res.currency').compute(cr, uid, frm_cur, to_cur, purchase_price, round=False, context=ctx)
    #         res['value'].update({'purchase_price': price})
    #     return res	
	
	def _product_purchase_margin(self, cr, uid, ids, field_name, arg, context=None):
		cur_obj = self.pool.get('res.currency')   # Lay object co ten la 'res.currency'
		res = {}
		for line in self.browse(cr, uid, ids, context=context):
			cur = line.order_id.pricelist_id.currency_id  # order_id (purchase_order_line) la field mapping vs field order_line (purchase_order)
			res[line.id] = 0
			if line.product_id:
				# tmp_margin = 10000
				tmp_margin = (line.product_id.list_price - line.product_id.standard_price) * line.product_qty
				res[line.id] = cur_obj.round(cr, uid, cur, tmp_margin)
		return res

	_columns = {
		'margin': fields.function(_product_purchase_margin, string='Margin', digits_compute= dp.get_precision('Product Price'),
			store = True),
		# 'purchase_price': fields.float('Cost Price', digits_compute= dp.get_precision('Product Price'))
	}


class purchase_order(osv.osv):
	_inherit = "purchase.order"

	def _product_purchase_margin(self, cr, uid, ids, field_name, arg, context=None):
		result = {}
		for purchase in self.browse(cr, uid, ids, context=context):
			result[purchase.id] = 0.0
			for line in purchase.order_line:
				#<t>cmt of SY(continue: bo qua dieu kien state 'cancel' va bat buoc lan lap tiep theo cua vong lap) 
				if line.state == 'cancel':
					continue
				#</t>
				# val += line.margin <ko khai bao dc val beacause phu thuoc vao recorde hien tai (purchase.id) => khi edit 1 purchase order se tao 1 recorde moi>
				# 1 recorde new <=> 1 purchase.id new
				# result[purchase.id]['margin'] = cur_obj.round(cr, uid, cur, val)
				result[purchase.id] += line.margin
		return result

	def _get_order(self, cr, uid, ids, context=None):
		result = {}
		for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
			result[line.order_id.id] = True
		return result.keys()

	_columns = {
		'margin': fields.function(_product_purchase_margin, string='Margin', help="It gives profitability by calculating the difference between the Unit Price and the cost price.", 
			store={				
				'purchase.order.line': (_get_order, ['margin','order_id'], 20),
				'purchase.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 20),
				}, digits_compute= dp.get_precision('Product Price')),
	}

