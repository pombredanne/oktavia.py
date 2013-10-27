'''
self is a Python version of shellinford library:
https://code.google.com/p/shellinford/

License: http://shibu.mit-license.org/
'''

from . import binaryio
import math
import array

class BitVector(object):
    SMALL_BLOCK_SIZE =  32
    LARGE_BLOCK_SIZE = 256
    BLOCK_RATE       =   8

    def __init__(self):
        self._r = array.array('L')
        self._v = array.array('L')
        self.clear()

    def build(self):
        self._size1 = 0
        for i, value in enumerate(self._v):    
            if i % BitVector.BLOCK_RATE == 0:
                self._r.append(self.size1())
            self._size1 += self._rank32(self._v[i], BitVector.SMALL_BLOCK_SIZE, True)

    def clear(self):
        del self._v[:]
        del self._r[:]
        self._size = 0
        self._size1 = 0

    def size(self):
        return self._size

    def size0(self):
        '''
        :return: size
        :rtype: int
        '''
        return self._size - self._size1

    def size1(self):
        '''
        :return: size
        :rtype: int
        '''
        return self._size1

    def set(self, value, flag = True):
        '''
        :param value: value
        :type  value: int
        :param flag: flag
        :type  flag: bool
        '''
        if value >= self.size():
            self._size = value + 1
        
        q = value // BitVector.SMALL_BLOCK_SIZE
        r = value % BitVector.SMALL_BLOCK_SIZE
        while q >= len(self._v):
            self._v.append(0)
        m = 0x1 << r
        if flag:
            self._v[q] |=  m
        else:
            self._v[q] &= ~m

    def get(self, value):
        '''
        :param value: value
        :type  value: int
        :return: bit
        :rtype: bool
        '''
        if value >= self.size():
            raise RangeError("BitVector.get() : range error")
        q = value // BitVector.SMALL_BLOCK_SIZE
        r = value % BitVector.SMALL_BLOCK_SIZE
        m  = 0x1 << r
        return bool(self._v[q] & m)

    def rank (self, i, b = True):
        '''
        :param i: position
        :type  i: int
        :param b: invert
        :type  b: bool
        :return: rank value
        :rtype: int
        '''
        if i > self.size():
            raise RangeError("BitVector.rank() : range error")
        if i == 0:
            return 0
        i -= 1
        q_large = math.floor(i // BitVector.LARGE_BLOCK_SIZE)
        q_small = math.floor(i // BitVector.SMALL_BLOCK_SIZE)
        r       = math.floor(i % BitVector.SMALL_BLOCK_SIZE)
        rank = self._r[q_large]
        if not b:
            rank = q_large * BitVector.LARGE_BLOCK_SIZE - rank
        begin = q_large * BitVector.BLOCK_RATE
        for j in range(begin, q_small):
            rank += self._rank32(self._v[j], BitVector.SMALL_BLOCK_SIZE, b)
        rank += self._rank32(self._v[q_small], r + 1, b)
        return rank

    def select(self, i, b = True):
        '''
        :param i: i
        :type  i: int
        :param b: b
        :type  b: bool
        :return: result
        :rtype: int
        '''
        if b:
            if i >= self.size1():
                raise RangeError("BitVector.select() : range error")
        elif i >= self.size0(): 
            raise RangeError("BitVector.select() : range error")
        left = 0
        right = len(self._r)
        while left < right:
            pivot = math.floor((left + right) // 2)
            rank  = self._r[pivot]
            if not b:
                rank = pivot * BitVector.LARGE_BLOCK_SIZE - rank
            if i < rank:
                right = pivot
            else:
                left = pivot + 1
        right -= 1
        if b:
            i -= self._r[right]
        else:
            i -= right * BitVector.LARGE_BLOCK_SIZE - self._r[right]
        j = right * BitVector.BLOCK_RATE
        while True:
            rank = self._rank32(self._v[j], BitVector.SMALL_BLOCK_SIZE, b)
            if i < rank:
                break
            j += 1
            i -= rank
        return j * BitVector.SMALL_BLOCK_SIZE + self._select32(self._v[j], i, b)

    def _rank32(self, x, i, b):
        '''
        :param x: x
        :type  x: int
        :param i: i
        :type  i: int
        :param b: b
        :type  b: bool
        '''
        if not b:
            x = ~x
        
        x <<= (BitVector.SMALL_BLOCK_SIZE - i)
        x = ((x & 0xaaaaaaaa) >>  1) + (x & 0x55555555)
        x = ((x & 0xcccccccc) >>  2) + (x & 0x33333333)
        x = ((x & 0xf0f0f0f0) >>  4) + (x & 0x0f0f0f0f)
        x = ((x & 0xff00ff00) >>  8) + (x & 0x00ff00ff)
        x = ((x & 0xffff0000) >> 16) + (x & 0x0000ffff)
        return x
    

    def _select32(self, x, i, b):
        '''
        :param x: x
        :type  x: int
        :param i: i
        :type  i: int
        :param b: b
        :type  b: bool
        '''
        if not b:
            x = ~x
        x1 = ((x  & 0xaaaaaaaa) >>  1) + (x  & 0x55555555)
        x2 = ((x1 & 0xcccccccc) >>  2) + (x1 & 0x33333333)
        x3 = ((x2 & 0xf0f0f0f0) >>  4) + (x2 & 0x0f0f0f0f)
        x4 = ((x3 & 0xff00ff00) >>  8) + (x3 & 0x00ff00ff)
        x5 = ((x4 & 0xffff0000) >> 16) + (x4 & 0x0000ffff)
        i += 1
        pos = 0
        v5 = x5 & 0xffffffff
        if i > v5:
            i -= v5
            pos += 32
        v4 = (x4 >> pos) & 0x0000ffff
        if i > v4:
            i -= v4
            pos += 16
        v3 = (x3 >> pos) & 0x000000ff
        if i > v3:
            i -= v3
            pos += 8
        v2 = (x2 >> pos) & 0x0000000f
        if i > v2:
            i -= v2
            pos += 4
        v1 = (x1 >> pos) & 0x00000003
        if i > v1:
            i -= v1
            pos += 2
        v0 = (x >> pos) & 0x00000001
        if i > v0:
            i -= v0
            pos += 1
        return pos

    def dump(self, output):
        '''
        :param output: output
        :type  output: BinaryOutput
        '''
        output.dump_32bit_number(self._size)
        output.dump_32bit_number_list(self._v.tolist())

    def load(self, input):
        '''
        :param input: input
        :type  input: BinaryInput
        '''
        self.clear()
        self._size = input.load_32bit_number()
        result = input.load_32bit_number_list()
        self._v.fromlist(result)
        self.build()