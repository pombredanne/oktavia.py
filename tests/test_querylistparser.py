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

from oktavia.queryparser import QueryListParser


class QueryListParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = QueryListParser()

    def test_and(self):
        self.parser.parse(['word1', 'word2'])
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertFalse(self.parser.queries[1].OR)
        self.assertFalse(self.parser.queries[1].NOT)
        self.assertFalse(self.parser.queries[1].RAW)

    def test_or(self):
        self.parser.parse(['word1', 'OR', 'word2'])
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertTrue(self.parser.queries[1].OR)
        self.assertFalse(self.parser.queries[1].NOT)
        self.assertFalse(self.parser.queries[1].RAW)

    def test_not(self):
        self.parser.parse(['word1', '-word2'])
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertFalse(self.parser.queries[1].OR)
        self.assertTrue(self.parser.queries[1].NOT)
        self.assertFalse(self.parser.queries[1].RAW)

    def test_raw(self):
        self.parser.parse(['word1', '"word2"'])
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertFalse(self.parser.queries[1].OR)
        self.assertFalse(self.parser.queries[1].NOT)
        self.assertTrue(self.parser.queries[1].RAW)

    def test_raw_not(self):
        self.parser.parse(['word1', '-"word2"'])
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertFalse(self.parser.queries[1].OR)
        self.assertTrue(self.parser.queries[1].NOT)
        self.assertTrue(self.parser.queries[1].RAW)
