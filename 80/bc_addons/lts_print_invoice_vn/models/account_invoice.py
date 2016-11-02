# -*- coding: utf-8 -*-
##############################################################################
#
#    @package lt_print_voucher_vn Vietname Print Account Invoice Odoo 8.0
#    @copyright Copyright (C) 2016 Lương Tien Sy (sy.luong@bluecom.vn). All rights reserved.#
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
from openerp import fields, models, api
# from gi.overrides.keysyms import currency

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    def _word(self, number):
        return {
            '0': 'không',
            '1': 'một',
            '2': 'hai',
            '3': 'ba',
            '4': 'bốn',
            '5': 'năm',
            '6': 'sáu',
            '7': 'bảy',
            '8': 'tám',
            '9': 'chín',
        }[number]
    
    def _unit(self, number_of_digits):
        return {
            '1': '',
            '2': 'nghìn',
            '3': 'triệu',
            '4': 'tỷ',            
            '5': 'nghìn',
            '6': 'triệu',
            '7': 'tỷ ',
        }[number_of_digits]
        
    def _split_mod(self, value):
        res = ''
        
        if value == '000':
            return ''
        if len(value) == 3:
            tr = value[:1]
            ch = value[1:2]
            dv = value[2:3]
            if tr == '0' and ch == '0':
                res = self._word(dv) + ' '
            if tr != '0' and ch == '0' and dv == '0':
                res = self._word(tr) + ' trăm '
            if tr != '0' and ch == '0' and dv != '0':
                res = self._word(tr) + ' trăm lẻ ' + self._word(dv) + ' '
            if tr == '0' and int(ch) > 1 and int(dv) > 0 and dv != '5':
                res = self._word(ch) + ' mươi ' + self._word(dv)
            if tr == '0' and int(ch) > 1 and dv == '0':
                res = self._word(ch) + ' mươi '
            if tr == '0' and int(ch) > 1 and dv == '5':
                res = self._word(ch) + ' mươi lăm '
            if tr == '0' and ch == '1' and int(dv) > 0 and dv != '5':
                res = ' mười ' + self._word(dv) + ' '
            if tr == '0' and ch == '1' and dv == '0':
                res = ' mười '
            if tr == '0' and ch == '1' and dv == '5':
                res = ' mười lăm '
            if int(tr) > 0 and int(ch) > 1 and int(dv) > 0 and dv != '5':
                res = self._word(tr) + ' trăm ' + self._word(ch) + ' mươi ' + self._word(dv) + ' '
            if int(tr) > 0 and int(ch) > 1 and dv == '0':
                res = self._word(tr) + ' trăm ' + self._word(ch) + ' mươi '
            if int(tr) > 0 and int(ch) > 1 and dv == '5':
                res = self._word(tr) + ' trăm ' + self._word(ch) + ' mươi lăm '
            if int(tr) > 0 and ch == '1' and int(dv) > 0 and dv != '5':
                res = self._word(tr) + ' trăm mười ' + self._word(dv) + ' '
            if int(tr) > 0 and ch == '1' and dv == '0':
                res = self._word(tr) + ' trăm mười '
            if int(tr) > 0 and ch == '1' and dv == '5':
                res = self._word(tr) + ' trăm mười lăm '                 
        
        return res
    
    def _split(self, value):
        res = ''
        
        if value == '000':
            return ''
        if len(value) == 3:
            tr = value[:1]
            ch = value[1:2]
            dv = value[2:3]
            if tr == '0' and ch == '0':
                res = ' không trăm lẻ ' + self._word(dv) + ' '
            if tr != '0' and ch == '0' and dv == '0':
                res = self._word(tr) + ' trăm '
            if tr != '0' and ch == '0' and dv != '0':
                res = self._word(tr) + ' trăm lẻ ' + self._word(dv) + ' '
            if tr == '0' and int(ch) > 1 and int(dv) > 0 and dv != '5':
                if int(dv) == 1:
                    res = ' không trăm ' + self._word(ch) + ' mươi mốt'
                else:
                    res = ' không trăm ' + self._word(ch) + ' mươi ' + self._word(dv)
            if tr == '0' and int(ch) > 1 and dv == '0':
                res = ' không trăm ' + self._word(ch) + ' mươi '
            if tr == '0' and int(ch) > 1 and dv == '5':
                res = ' không trăm ' + self._word(ch) + ' mươi lăm '
            if tr == '0' and ch == '1' and int(dv) > 0 and dv != '5':
                res = ' không trăm mười ' + self._word(dv)
            if tr == '0' and ch == '1' and dv == '0':
                res = ' không trăm mười '
            if tr == '0' and ch == '1' and dv == '5':
                res = ' không trăm mười lăm '
            if int(tr) > 0 and int(ch) > 1 and int(dv) > 0 and dv != '5':
                if int(dv) == 1:
                    res = self._word(tr) + ' trăm ' + self._word(ch) + ' mươi mốt'
                else:
                    res = self._word(tr) + ' trăm ' + self._word(ch) + ' mươi ' + self._word(dv) + ' '
            if int(tr) > 0 and int(ch) > 1 and dv == '0':
                res = self._word(tr) + ' trăm ' + self._word(ch) + ' mươi '
            if int(tr) > 0 and int(ch) > 1 and dv == '5':
                res = self._word(tr) + ' trăm ' + self._word(ch) + ' mươi lăm '
            if int(tr) > 0 and ch == '1' and int(dv) > 0 and dv != '5':
                res = self._word(tr) + ' trăm mười ' + self._word(dv) + ' '
            if int(tr) > 0 and ch == '1' and dv == '0':
                res = self._word(tr) + ' trăm mười '
            if int(tr) > 0 and ch == '1' and dv == '5':
                res = self._word(tr) + ' trăm mười lăm '                 
        
        return res
    
    @api.one
    @api.depends('amount_total')
    def _num2word(self):
        amount_total = self.amount_total
        if amount_total == 0:
            self.lt_total_in_word = 'Không'
        else:
            #delare
            in_word = ''
            split_mod = ''
            split_remain = ''
            num = int(amount_total)
            decimal = amount_total - num
            gnum = str(num)
            gdecimal = str(decimal)[2:]
            m = int(len(gnum) / 3)
            mod = len(gnum) - m * 3
            sign = '[+]'
            
            # sign
            if amount_total < 0:
                sign = '[-]'
            else:
                sign = ''
                
            # tách hàng lớn nhất
            if mod == 1:
                split_mod = '00' + str(num)[:1]
            elif mod == 2:
                split_mod = '0' + str(num)[:2]
            elif mod == 0:
                split_mod = '000'
            # tách hàng còn lại sau mod
            if len(str(num)) > 2:
                split_remain = str(num)[mod:]
            # đơn vị hàng mod
            im = m + 1
            if mod > 0:
                in_word = self._split_mod(split_mod) + ' ' + self._unit(str(im))
            # tách 3 trong split_remain
            i = m
            _m = m
            j = 1
            split3 = ''
            split3_ = ''
            while i > 0:
                split3 = split_remain[:3]
                split3_ = split3
                in_word = in_word + ' ' + self._split(split3)
                m = _m + 1 - j
                if int(split3_) != 0:
                    in_word = in_word + ' ' + self._unit(str(m))
                split_remain = split_remain[3:]
                i = i - 1
                j = j + 1 
            if in_word[:1] == 'k':
                in_word = in_word[10:]
            if in_word[:1] == 'l':
                in_word = in_word[2:]
            if len(in_word) > 0:
                in_word = sign + ' ' + str(in_word.strip()[:1]).upper() + in_word.strip()[1:]
    
            if decimal > 0:
                in_word += ' phẩy'
                for i in range(0, len(gdecimal)):
                    in_word += ' ' + self._word(gdecimal[i])
    
            self.lt_total_in_word = in_word
    
    lt_reason = fields.Char(string="Reason", size=256)
    lt_no_of_origin = fields.Integer(string="No. of Origin", size=50, help="Number of the origin documents, to be displayed on the PDF printed version of this document.")
    lt_recipient_payer = fields.Char(string="Recipient / Payer")
    lt_total_in_word = fields.Char(string="In word", compute='_num2word', store=False)
    
#     _columns = {
#         'reason':fields.char('Reason', size=256),
#         'no_of_origin': fields.integer('No. of Origin', size=50, help="Number of the origin documents, to be displayed on the PDF printed version of this document."),
#         'recipient_payer': fields.char('Recipient / Payer'),
#         'total_in_word': fields.function(_num2word, method=True, type='char', string='In word', store=False),
#         'decision_type': fields.function(_get_decision_type, method=True, type='char', string='In word', store=False),
#     }
