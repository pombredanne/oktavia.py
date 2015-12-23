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

"""
Test data generator script to test compatibility with binary-io.jsx
"""

from __future__ import absolute_import, print_function

import os
import sys

import oktavia


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

output = oktavia.binaryio.BinaryOutput()

output.dump_16bit_number(0)
output.dump_16bit_number(65535)
output.dump_32bit_number(0)
output.dump_32bit_number(4294967295)
output.dump_string('hello world')
output.dump_string_list(['hello', 'world'])
output.dump_string_list_map({'hello': ['HELLO'], 'world': ['WORLD']})
output.dump_32bit_number_list([0, 0, 0, 0, 0])

out = open('testdata.bin', 'bw')
out.write(output.result())
out.close()
