# MIT License
#
# Copyright (c) 2020 Christopher Friedt
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

'''The HanoiState Class

The HanoiState Class encapsulates information for 1 instance of the classic
Towers of Hanoi puzzle.

https://en.wikipedia.org/wiki/Tower_of_Hanoi

The optimal solution to the Towers of Hanoi requires 2^N - 1 moves. Thus, the
time complexity is O(2^N). The memory requirements are O(N), where N is the
number of discs.

Currently a maximum of 64 discs are 'supported'. I say that loosely because
it could take an extremely long amount of time for a single computer to solve
the problem when N is 64.

The way that this object keeps track of the state of the 3 towers is by encoding
each disc as a bit in an unsigned integer. Specifically, disc N is represented by
bit N - 1 of any given tower.

Towers are numbered 0 to 2.

This class itself does not have methods, so it's more like a data aggregate.

To operate on a HanoiState instance, use the Hanoi Class. 
'''

from threading import Lock

counterLock = Lock()
counter = 0


class HanoiState(object):

    def __init__(self, numberOfDiscs=4, source=0, target=2):
        '''Initialize a HanoiState object

        Upon initialization, numberOfDiscs discs are placed on
        source, other towers are empty, and the number of
        moves is set to 0.

        :param numberOfDiscs: the number of discs in the game
        :param source: the tower from which discs should be moved
        :param target: the tower to which discs should be moved
        '''

        global counter

        # check arguments
        if numberOfDiscs <= 0 or numberOfDiscs > 64:
            raise ValueError(
                'numberOfDiscs {} is invalid'.format(numberOfDiscs))
        if source < 0 or source > 2:
            raise ValueError('source {} is invalid'.format(source))
        if target < 0 or target > 2:
            raise ValueError('target {} is invalid'.format(target))
        if source == target:
            raise ValueError('source may not equal target')

        counterLock.acquire()
        self.id = counter
        counter += 1
        counterLock.release()

        self.numberOfDiscs = numberOfDiscs
        self.tower = [0, 0, 0]
        self.tower[source] = (1 << numberOfDiscs) - 1
        self.source = source
        self.target = target
        self.numberOfMoves = 0

    def to_json(self):
        s = ''
        s += '{'
        s += '"sessionId": {}'.format(self.id) + ', '
        s += '"numberOfDiscs": {}'.format(self.numberOfDiscs) + ', '
        s += '"fromTower": {}'.format(self.source) + ', '
        s += '"toTower": {}'.format(self.target) + ', '
        s += '"numberOfMoves": {}'.format(self.numberOfMoves) + ', '
        s += '"towers": {}'.format(self.tower)
        s += '}'
        return s
