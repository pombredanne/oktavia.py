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

import snowballstemmer

from oktavia.oktavia import Oktavia


class StemmingTest(unittest.TestCase):
    def setUp(self):
        self.oktavia = Oktavia()
        self.oktavia.set_stemmer(snowballstemmer.EnglishStemmer())
        self.section = self.oktavia.add_section(u'document')
        self.oktavia.add_word(u'stemming baby', stemming=True)
        self.section.set_tail(u'doc1')
        self.oktavia.add_word(u'stemmed babies', stemming=True)
        self.section.set_tail(u'doc2')
        self.oktavia.build()

    def test_search_without_stemming(self):
        results = self.oktavia.raw_search(u'baby', stemming=False)
        self.assertEqual(1, len(results))

    def test_search_with_stemming(self):
        results = self.oktavia.raw_search(u'baby', stemming=True)
        self.assertEqual(1, len(results))

    def test_load_dump_and_search_without_stemming(self):
        dump = self.oktavia.dump()
        oktavia = Oktavia()
        oktavia.set_stemmer(snowballstemmer.EnglishStemmer())
        oktavia.load(dump)
        results = oktavia.raw_search(u'baby', stemming=False)
        self.assertEqual(1, len(results))

    def test_load_dump_and_search_with_stemming(self):
        dump = self.oktavia.dump()
        oktavia = Oktavia()
        oktavia.set_stemmer(snowballstemmer.EnglishStemmer())
        oktavia.load(dump)
        results = oktavia.raw_search(u'baby', stemming=True)
        self.assertEqual(1, len(results))
