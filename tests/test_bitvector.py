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

from oktavia.bitvector import BitVector

try:
    from oktavia import _bitvector as native_bitvector
except ImportError:
    native_bitvector = None


if native_bitvector:
    NativeBitVector = native_bitvector.BitVector
    class NativeBitVectorText(unittest.TestCase):
        def setUp(self):
            self.bv0 = NativeBitVector()
            self.bv1 = NativeBitVector()
            self.src_values = [0, 511, 512, 1000, 2000, 3000]

            for i in range(self.src_values[-1]):
                self.bv0.set(i, True)

            for v in self.src_values:
                self.bv1.set(v, True)
                self.bv0.set(v, False)

            self.bv1.build()
            self.bv0.build()

        def test_size(self):
            self.assertEqual(self.src_values[-1] + 1, self.bv1.size())  # = 3001
            self.assertEqual(len(self.src_values), self.bv1.size1())  # = 6
            self.assertEqual(self.src_values[-1] + 1, self.bv0.size())  # = 3001
            self.assertEqual(len(self.src_values), self.bv0.size0())  # = 6

        def test_get(self):
            for v in self.src_values:
                self.assertTrue(self.bv1.get(v))
                self.assertFalse(self.bv0.get(v))

        def test_rank(self):
            for i, v in enumerate(self.src_values):
                self.assertEqual(i, self.bv1.rank(v, True))
                self.assertEqual(i, self.bv0.rank(v, False))

        def test_select(self):
            for i, v in enumerate(self.src_values):
                self.assertEqual(v, self.bv1.select(i, True))
                self.assertEqual(v, self.bv0.select(i, False))


class BitVectorTest(unittest.TestCase):

    def setUp(self):
        self.bv0 = BitVector()
        self.bv1 = BitVector()
        self.src_values = [0, 511, 512, 1000, 2000, 3000]

        for i in range(self.src_values[-1]):
            self.bv0.set(i, True)

        for v in self.src_values:
            self.bv1.set(v, True)
            self.bv0.set(v, False)

        self.bv1.build()
        self.bv0.build()

    def test_size(self):
        self.assertEqual(self.src_values[-1] + 1, self.bv1.size())  # = 3001
        self.assertEqual(len(self.src_values), self.bv1.size1())  # = 6
        self.assertEqual(self.src_values[-1] + 1, self.bv0.size())  # = 3001
        self.assertEqual(len(self.src_values), self.bv0.size0())  # = 6

    def test_get(self):
        for v in self.src_values:
            self.assertTrue(self.bv1.get(v))
            self.assertFalse(self.bv0.get(v))

    def test_rank(self):
        for i, v in enumerate(self.src_values):
            self.assertEqual(i, self.bv1.rank(v, True))
            self.assertEqual(i, self.bv0.rank(v, False))

    def test_select(self):
        for i, v in enumerate(self.src_values):
            self.assertEqual(v, self.bv1.select(i, True))
            self.assertEqual(v, self.bv0.select(i, False))

    def test_load_dump_and_size(self):
        dump1 = BinaryOutput()
        dump0 = BinaryOutput()
        self.bv1.dump(dump1)
        self.bv0.dump(dump0)
        self.bv1.load(BinaryInput(dump1.result()))
        self.bv0.load(BinaryInput(dump0.result()))

        self.assertEqual(self.src_values[-1] + 1, self.bv1.size())
        self.assertEqual(len(self.src_values), self.bv1.size1())
        self.assertEqual(self.src_values[-1] + 1, self.bv0.size())
        self.assertEqual(len(self.src_values), self.bv0.size0())

    def test_load_dump_and_get(self):
        dump1 = BinaryOutput()
        dump0 = BinaryOutput()
        self.bv1.dump(dump1)
        self.bv0.dump(dump0)
        self.bv1.load(BinaryInput(dump1.result()))
        self.bv0.load(BinaryInput(dump0.result()))

        for v in self.src_values:
            self.assertTrue(self.bv1.get(v))
            self.assertFalse(self.bv0.get(v))

    def test_load_dump_and_rank(self):
        dump1 = BinaryOutput()
        dump0 = BinaryOutput()
        self.bv1.dump(dump1)
        self.bv0.dump(dump0)
        self.bv1.load(BinaryInput(dump1.result()))
        self.bv0.load(BinaryInput(dump0.result()))

        for i, v in enumerate(self.src_values):
            self.assertEqual(i, self.bv1.rank(v, True))
            self.assertEqual(i, self.bv0.rank(v, False))

    def test_load_dump_and_select(self):
        dump1 = BinaryOutput()
        dump0 = BinaryOutput()
        self.bv1.dump(dump1)
        self.bv0.dump(dump0)
        self.bv1.load(BinaryInput(dump1.result()))
        self.bv0.load(BinaryInput(dump0.result()))

        for i, v in enumerate(self.src_values):
            self.assertEqual(v, self.bv1.select(i, True))
            self.assertEqual(v, self.bv0.select(i, False))
