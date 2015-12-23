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

import sys


from . sais import SAIS
from oktavia import RangeError

_range = range if sys.version_info[0] == 3 else xrange

class BWT(object):

    END_MARKER = chr(0)
    END_MARKER_CODE = 0

    def __init__(self, string, rawmode=False):
        self._rawmode = rawmode
        if rawmode:
            str2 = string + [0]
            self._str = str2
            self._size = len(self._str)
            self._suffixarray = SAIS.make(str2, rawmode=True)
            self._head = self._suffixarray.index(0)
        else:
            str2 = string + BWT.END_MARKER
            self._str = str2
            self._size = len(self._str)
            self._suffixarray = SAIS.make(str2)
            self._head = self._suffixarray.index(0)

    def size(self):
        return self._size

    def head(self):
        return self._head

    def clear(self):
        self._str = ''
        self._size = 0
        self._head = 0
        del self._suffixarray[:]

    def get(self, i=None, replace=None):
        if i is None:
            size = self.size()
            chars = [self.get(i) for i in _range(size)]
            if self._rawmode:
                result = chars
                if replace is not None:
                    while BWT.END_MARKER_CODE in replace:
                        index = result.index(BWT.END_MARKER_CODE)
                        result[index] = replace
            else:
                result = ''.join(chars)
                if replace is not None:
                    result = result.replace(BWT.END_MARKER, replace)
        else:
            size = self.size()
            if i >= size:
                raise RangeError('BWT.get() : range error')
            index = (self._suffixarray[i] + size - 1) % size
            result = self._str[index]
        return result

def bwt(string, endMarker=None):
    bwt = BWT(string)
    return bwt.get(replace=endMarker)
