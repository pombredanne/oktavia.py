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

from oktavia.binaryio import BinaryInput
from oktavia.binaryio import BinaryOutput
from oktavia.waveletmatrix import WaveletMatrix


class WaveletMatrixTest(unittest.TestCase):

    def setUp(self):
        self.test_src = 'abracadabra mississippi'
        self.wm = WaveletMatrix()
        self.wm.build(self.test_src)
        self.rd = []
        self.sd = []
        self.td = []

        for i in range(256):
            self.rd.append([0])
            self.td.append([0])
            self.sd.append([])

        for i in range(len(self.test_src)):
            for c in range(256):
                self.rd[c].append(self.rd[c][i])
                self.td[c].append(self.td[c][i])
                if ord(self.test_src[i]) == c:
                    self.rd[c][i + 1] += 1
                    self.sd[c].append(i)
                if ord(self.test_src[i]) < c:
                    self.td[c][i + 1] += 1

    def test_size_and_count(self):
        self.assertEqual(len(self.test_src), self.wm.size())
        for c in range(256):
            self.assertEqual(self.rd[c][self.wm.size()], self.wm.count(c))

    def test_get(self):
        for i in range(self.wm.size()):
            self.assertEqual(ord(self.test_src[i]), self.wm.get(i))

    def test_rank(self):
        for c in range(256):
            for i in range(self.wm.size()):
                self.assertEqual(self.rd[c][i], self.wm.rank(i, c))

    def test_rank_less_than(self):
        for c in range(256):
            for i in range(self.wm.size()):
                self.assertEqual(self.td[c][i], self.wm.rank_less_than(i, c))

    def test_load_dump_and_size_and_count(self):
        dump = BinaryOutput()
        self.wm.dump(dump)
        self.wm.load(BinaryInput(dump.result()))

        self.assertEqual(len(self.test_src), self.wm.size())
        for c in range(256):
            self.assertEqual(self.rd[c][self.wm.size()], self.wm.count(c))

    def test_load_dump_and_get(self):
        dump = BinaryOutput()
        self.wm.dump(dump)
        self.wm.load(BinaryInput(dump.result()))

        for i in range(self.wm.size()):
            self.assertEqual(ord(self.test_src[i]), self.wm.get(i))

    def test_load_dump_and_rank(self):
        dump = BinaryOutput()
        self.wm.dump(dump)
        self.wm.load(BinaryInput(dump.result()))

        for c in range(256):
            for i in range(self.wm.size()):
                self.assertEqual(self.rd[c][i], self.wm.rank(i, c))

    def test_load_dump_and_rank_less_than(self):
        dump = BinaryOutput()
        self.wm.dump(dump)
        self.wm.load(BinaryInput(dump.result()))

        for c in range(256):
            for i in range(self.wm.size()):
                self.assertEqual(self.td[c][i], self.wm.rank_less_than(i, c))

    def test_simple_usage(self):
        self.assertEqual(4, self.wm.rank(10, ord('a')))
