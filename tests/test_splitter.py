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


class SplitterTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.splitter = self.oktavia.add_splitter('document')
        self.oktavia.add_word('abracadabra')
        self.splitter.split()
        self.oktavia.add_word('mississippi')
        self.splitter.split()
        self.oktavia.add_word('abracadabra mississippi')
        self.splitter.split()
        self.oktavia.build(5)

    def test_count(self):
        self.assertEqual(3, self.splitter.size())

    def test_get_splitter_index(self):
        self.assertEqual(0, self.splitter.get_index(0))
        self.assertEqual(0, self.splitter.get_index(10))
        self.assertEqual(1, self.splitter.get_index(11))
        self.assertEqual(1, self.splitter.get_index(21))
        self.assertEqual(2, self.splitter.get_index(22))
        self.assertEqual(2, self.splitter.get_index(44))

    def test_get_splitter_index_boundary(self):
        try:
            self.splitter.get_index(-1)
            self.fail('fm.get_index()')
        except:
            pass
        try:
            self.splitter.get_index(45)
            self.fail('fm.get_index()')
        except:
            pass

    def test_get_splitter_content(self):
        self.assertEqual('abracadabra mississippi', self.splitter.get_content(2))
        self.assertEqual('mississippi', self.splitter.get_content(1))
        self.assertEqual('abracadabra', self.splitter.get_content(0))

    def test_get_splitter_content_boundary(self):
        try:
            self.splitter.get_content(3)
            self.fail('fm.get_content()')
        except:
            pass
        try:
            self.splitter.get_content(-1)
            self.fail('fm.get_content()')
        except:
            pass

    def test_load_dump_and_count(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.get_splitter('document')
        self.assertEqual(3, self.splitter.size())

    def test_load_dump_and_get_splitter_index(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.get_splitter('document')

        self.assertEqual(0, self.splitter.get_index(0))
        self.assertEqual(0, self.splitter.get_index(10))
        self.assertEqual(1, self.splitter.get_index(11))
        self.assertEqual(1, self.splitter.get_index(21))
        self.assertEqual(2, self.splitter.get_index(22))
        self.assertEqual(2, self.splitter.get_index(44))

    def test_load_dump_and_get_splitter_index_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.get_splitter('document')

        try:
            self.splitter.get_index(-1)
            self.fail('fm.get_index()')
        except:
            pass
        try:
            self.splitter.get_index(45)
            self.fail('fm.get_index()')
        except:
            pass

    def test_load_dump_and_get_splitter_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.get_splitter('document')

        self.assertEqual('abracadabra mississippi', self.splitter.get_content(2))
        self.assertEqual('mississippi', self.splitter.get_content(1))
        self.assertEqual('abracadabra', self.splitter.get_content(0))

    def test_load_dump_and_get_splitter_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.get_splitter('document')

        try:
            self.splitter.get_content(3)
            self.fail('fm.get_content()')
        except:
            pass
        try:
            self.splitter.get_content(-1)
            self.fail('fm.get_content()')
        except:
            pass
