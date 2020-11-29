# MIT License
#
# Copyright (c) 2018 Christopher Friedt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import threading

from hanoi import HanoiState

'''The Hanoi Class

The Hanoi Class provides a means to operate on a HanoiState instance.

Supported operations are:

numberOfMoves = solve()
move(source, target)
state = getState()
'''


class Hanoi(object):

    @staticmethod
    def popcount(x):
        '''Count the number of set bits in an unsigned integer.
        Like the GCC builtin __builtin_popcount(), or 'population count'
        See https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html
        '''
        r = 0
        while x:
            if x & 1:
                r += 1
            x >>= 1
        return r

    @staticmethod
    def fls(x):
        '''Find the last set bit of an unsigned integer
        More specifically, this function returns the least-significant set bit.
        '''
        if not x:
            raise ValueError('fls should not be called with x == 0')

        r = 0
        while not (x & 1):
            x >>= 1
            r += 1
        return r

    def __init__(self, numberOfDiscs, source, target):
        '''Initialize a Hanoi object'''
        self._state = HanoiState(numberOfDiscs, source, target)
        self._lock = threading.Lock()

    def getState(self, timeout=-1):
        '''Get a copy of the internal state'''
        locked = self._lock.acquire(timeout=timeout)
        if locked:
            s = self._state
            self._lock.release()
        else:
            raise TimeoutError()
        return s

    def move(self, source, target, timeout=-1):
        '''Move the top disc from source to target'''
        if source < 0 or source > 2:
            raise ValueError('source {} is invalid'.format(source))
        if target < 0 or target > 2:
            raise ValueError('target {} is invalid'.format(target))
        if source == target:
            raise ValueError('source may not equal target')

        locked = self._lock.acquire(timeout=timeout)
        if locked:
            if Hanoi.popcount(self._state.tower[source]) == 0:
                raise ValueError('source {} is empty'.format(source))
            froN = Hanoi.fls(self._state.tower[source])
            if Hanoi.popcount(self._state.tower[target]) != 0:
                toN = Hanoi.fls(self._state.tower[target])
                # cannot put a larger disc on top of a smaller disc
                if froN > toN:
                    raise ValueError(
                        'cannot put disc {} on top of disc {}'.format(froN + 1, toN + 1))
            N = froN
            mask = 1 << N
            # remove disc N from the source tower
            self._state.tower[source] &= ~mask
            # add disc N to the target tower
            self._state.tower[target] |= mask
            self._state.numberOfMoves += 1
            self._lock.release()
        else:
            raise TimeoutError()

    def isComplete(self, timeout=-1):
        '''Get a copy of the internal state'''
        locked = self._lock.acquire(timeout=timeout)
        complete = False
        if locked:
            n = self._state.numberOfDiscs
            t = target = self._state.target
            complete = self._state.tower[t] == ((1 << n) - 1)
        else:
            raise TimeoutError()
        return complete
