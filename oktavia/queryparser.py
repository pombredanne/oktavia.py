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

import re

from .query import Query


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

class QueryParser(object):
    def highlight(self):
        """
        :rtype: string
        """
        result = []
        for query in self.queries:
            if not query.NOT:
                result.append(('highlight', query.word))
        return '?' + urlencode(result)


class QueryListParser(QueryParser):
    def __init__(self):
        self.queries = []

    def parse(self, queryStrings):
        """
        :param queryStrings: query
        :type  queryStrings: str[]
        :return: parsed query
        :rtype: Query[]
        """
        nextOr = False
        for word in queryStrings:
            if word == 'OR':
                nextOr = True
            else:
                query = Query()
                if nextOr:
                    query.OR = True
                    nextOr = False
                if word.startswith('-'):
                    query.NOT = True
                    word = word[1:]
                if word.startswith('"') and word.endswith('"'):
                    query.RAW = True
                    word = word[1:-1]
                query.word = word
                self.queries.append(query)
        return self.queries


class QueryStringParser(QueryParser):
    def __init__(self):
        self.queries = []

    def parse(self, queryString):
        """
        :param queryString: query
        :type  queryString: str
        return: parsed query
        :rtype: Query[]
        """
        nextOr = False
        nextNot = False
        currentWordStart = 0
        status = 0
        # 0: free
        # 1: in unquoted word
        # 2: in quote
        isSpace = re.compile(r'[\s\u3000]')
        for i, ch in enumerate(queryString):
            if status == 0:  # free
                if not isSpace.match(ch):
                    if ch == '-':
                        nextNot = True
                    elif ch == '"':
                        currentWordStart = i + 1
                        status = 2
                    else:
                        currentWordStart = i
                        status = 1
                else:
                    nextNot = False
            elif status == 1:  # unquoted word
                if isSpace.match(ch):
                    word = queryString[currentWordStart:i]
                    if word == 'OR':
                        nextOr = True
                    else:
                        query = Query()
                        query.word = word
                        query.OR = nextOr
                        query.NOT = nextNot
                        self.queries.append(query)
                        nextOr = False
                        nextNot = False
                    status = 0
            elif status == 2:  # in quote
                if ch == '"':
                    word = queryString[currentWordStart:i]
                    query = Query()
                    query.word = word
                    query.OR = nextOr
                    query.NOT = nextNot
                    query.RAW = True
                    self.queries.append(query)
                    nextOr = False
                    nextNot = False
                    status = 0
        if status == 1:
            query = Query()
            word = queryString[currentWordStart:len(queryString)]
            if word != 'OR':
                query.word = word
                query.OR = nextOr
                query.NOT = nextNot
                self.queries.append(query)
        elif status == 2:
            query = Query()
            query.word = queryString[currentWordStart:currentWordStart + len(queryString)]
            query.OR = nextOr
            query.NOT = nextNot
            query.RAW = True
            self.queries.append(query)

        return self.queries
