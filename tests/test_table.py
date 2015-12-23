#
# http://shibu.mit-license.org/
#  The MIT License (MIT)
#
# Copyright (c) 2015 Yoshiki Shibukawa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import absolute_import, print_function, division

import unittest

from oktavia.oktavia import Oktavia


class TableTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.table = self.oktavia.add_table('address book', ['zip', 'city', 'area code'])

        self.oktavia.add_word('94101')  # 5
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word('San Francisco')  # 13
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word('415')  # 3
        self.table.set_column_tail_and_EOB()
        self.table.set_row_tail()

        self.oktavia.add_word('94607')  # 5
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word('Oakland')  # 7
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word('510')  # 3
        self.table.set_column_tail_and_EOB()
        self.table.set_row_tail()

        self.oktavia.add_word('94401')  # 5
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word('San Mateo')  # 9
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word('650')  # 3
        self.table.set_column_tail_and_EOB()
        self.table.set_row_tail()

        self.oktavia.build()

    def test_row_sizes(self):
        self.assertEqual(3, self.table.row_size())

    def test_column_sizes(self):
        self.assertEqual(3, self.table.column_size())

    def test_get_cell(self):
        self.assertEqual(0, self.table.get_cell(0)[0])
        self.assertEqual(0, self.table.get_cell(0)[1])
        self.assertEqual(0, self.table.get_cell(22)[0])
        self.assertEqual(2, self.table.get_cell(22)[1])
        self.assertEqual(1, self.table.get_cell(24)[0])
        self.assertEqual(0, self.table.get_cell(24)[1])
        self.assertEqual(1, self.table.get_cell(40)[0])
        self.assertEqual(2, self.table.get_cell(40)[1])
        self.assertEqual(2, self.table.get_cell(42)[0])
        self.assertEqual(0, self.table.get_cell(42)[1])
        self.assertEqual(2, self.table.get_cell(60)[0])
        self.assertEqual(2, self.table.get_cell(60)[1])

    def test_get_table_index_boundary(self):
        try:
            self.table.get_cell(-1)
            self.fail('fm.gettableIndex()')
        except:
            pass
        try:
            self.table.get_cell(62)
            self.fail('fm.gettableIndex()')
        except:
            pass

    def test_get_table_content(self):
        row = self.table.get_row_content(0)
        self.assertEqual('94101', row['zip'])
        self.assertEqual('San Francisco', row['city'])
        self.assertEqual('415', row['area code'])

    def test_get_table_content_boundary(self):
        try:
            self.table.get_content(3)
            self.fail('fm.get_content()')
        except:
            pass
        try:
            self.table.get_content(-1)
            self.fail('fm.get_content()')
        except:
            pass

    def test_load_dump_and_row_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')
        self.assertEqual(3, self.table.row_size())

    def test_load_dump_and_column_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        self.assertEqual(3, self.table.column_size())

    def test_load_dump_and_get_cell(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        self.assertEqual(0, self.table.get_cell(0)[0])
        self.assertEqual(0, self.table.get_cell(0)[1])
        self.assertEqual(0, self.table.get_cell(22)[0])
        self.assertEqual(2, self.table.get_cell(22)[1])
        self.assertEqual(1, self.table.get_cell(24)[0])
        self.assertEqual(0, self.table.get_cell(24)[1])
        self.assertEqual(1, self.table.get_cell(40)[0])
        self.assertEqual(2, self.table.get_cell(40)[1])
        self.assertEqual(2, self.table.get_cell(42)[0])
        self.assertEqual(0, self.table.get_cell(42)[1])
        self.assertEqual(2, self.table.get_cell(60)[0])
        self.assertEqual(2, self.table.get_cell(60)[1])

    def test_load_dump_and_get_table_index_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        try:
            self.table.get_cell(-1)
            self.fail('fm.gettableIndex()')
        except:
            pass
        try:
            self.table.get_cell(62)
            self.fail('fm.gettableIndex()')
        except:
            pass

    def test_load_dump_and_get_table_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        row = self.table.get_row_content(0)
        self.assertEqual('94101', row['zip'])
        self.assertEqual('San Francisco', row['city'])
        self.assertEqual('415', row['area code'])

    def test_load_dump_and_get_table_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        try:
            self.table.get_content(3)
            self.fail('fm.get_content()')
        except:
            pass
        try:
            self.table.get_content(-1)
            self.fail('fm.get_content()')
        except:
            pass
