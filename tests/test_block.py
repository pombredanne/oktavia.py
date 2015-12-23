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


class BlockTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.block = self.oktavia.add_block('document')
        self.oktavia.add_word('abracadabra')
        self.block.start_block('river')
        self.oktavia.add_word('mississippi')
        self.block.end_block()
        self.oktavia.add_word('abracadabra mississippi')
        self.oktavia.build()

    def test_doc_sizes(self):
        self.assertEqual(1, self.block.size())

    def test_in_block(self):
        self.assertFalse(self.block.in_block(0))
        self.assertFalse(self.block.in_block(10))
        self.assertTrue(self.block.in_block(11))
        self.assertTrue(self.block.in_block(21))
        self.assertFalse(self.block.in_block(22))
        self.assertFalse(self.block.in_block(44))

    def test_in_block_boundary(self):
        try:
            self.block.in_block(-1)
            self.fail('fm.in_block() 1')
        except:
            pass
        try:
            self.block.in_block(45)
            self.fail('fm.in_block() 2')
        except:
            pass

    def test_get_block_content(self):
        self.assertEqual('mississippi', self.block.get_block_content(11))

    def test_get_block_content_boundary(self):
        try:
            self.block.get_block_content(45)
            self.fail('fm.getContent()')
        except:
            pass
        try:
            self.block.get_block_content(-1)
            self.fail('fm.getContent()')
        except:
            pass

    def test_get_block_name(self):
        self.assertEqual('river', self.block.get_block_name(11))

    def test_get_block_name_boundary(self):
        try:
            self.block.get_block_name(45)
            self.fail('fm.getName()')
        except:
            pass
        try:
            self.block.get_block_name(-1)
            self.fail('fm.getName()')
        except:
            pass

    def test_dump_load_and_doc_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.get_block('document')

        self.assertEqual(1, self.block.size())

    def test_load_dump_and_in_block(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.get_block('document')

        self.assertFalse(self.block.in_block(0))
        self.assertFalse(self.block.in_block(10))
        self.assertTrue(self.block.in_block(11))
        self.assertTrue(self.block.in_block(21))
        self.assertFalse(self.block.in_block(22))
        self.assertFalse(self.block.in_block(44))

    def test_load_dump_and_in_block_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.get_block('document')

        try:
            self.block.in_block(-1)
            self.fail('fm.in_block() 1')
        except:
            pass
        try:
            self.block.in_block(45)
            self.fail('fm.in_block() 2')
        except:
            pass

    def test_load_dump_and_get_block_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.get_block('document')

        self.assertEqual('mississippi', self.block.get_block_content(11))

    def test_load_dump_and_get_block_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.get_block('document')

        try:
            self.block.get_block_content(45)
            self.fail('fm.getContent()')
        except:
            pass
        try:
            self.block.get_block_content(-1)
            self.fail('fm.getContent()')
        except:
            pass

    def test_load_dump_and_get_block_name(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.get_block('document')

        self.assertEqual('river', self.block.get_block_name(11))

    def test_load_dump_and_get_block_name_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.get_block('document')

        try:
            self.block.get_block_name(45)
            self.fail('fm.getName()')
        except:
            pass
        try:
            self.block.get_block_name(-1)
            self.fail('fm.getName()')
        except:
            pass
