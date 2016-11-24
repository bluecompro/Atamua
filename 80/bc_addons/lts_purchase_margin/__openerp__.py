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
{
    'name' : 'Bluecom Purchase',
    'version': '1.0',
    'author' : 'Luong Tien Sy',
    'summary': 'Custom Purchase Information',
    'website': 'http://bluecom.vn',
    'sequence': 30,
    'category': 'Hidden',
    'description':"""
Custom Purchase Information
==========================

    """,
    'depends': ['purchase'],
    'data': [
        'views/purchase_margin_view.xml',
    ],
    'installable': True,
    'application': False,
}

