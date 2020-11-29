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

import pytest

from hanoi import Hanoi


def test_popcount():
    assert 2 == Hanoi.popcount(0b101)


def test_fls_happy_path():
    assert 2 == Hanoi.fls(0b100)


def test_fls_zero():
    with pytest.raises(ValueError, match=r'fls should not be called with x == 0'):
        Hanoi.fls(0)


def test_init_happy_path():
    h = Hanoi(4, 0, 2)
    assert h
    assert not h._lock.locked()


def test_getState_happy_path():
    h = Hanoi(4, 0, 2)
    assert h.getState()


def test_getState_locked():
    h = Hanoi(4, 0, 2)
    h._lock.acquire()
    with pytest.raises(TimeoutError):
        h.getState(0)


def test_move_happy_path():
    h = Hanoi(4, 0, 2)
    assert h._state.tower[0] == 0b1111
    h.move(0, 1)
    # smallest disc / least-significant bit is moved
    assert h._state.tower[0] == 0b1110
    assert h._state.tower[1] == 0b0001
    h.move(0, 2)
    h.move(1, 2)
    h.move(0, 1)
    h.move(2, 0)
    h.move(2, 1)
    h.move(0, 1)
    h.move(0, 2)
    h.move(1, 2)
    h.move(1, 0)
    h.move(2, 0)
    h.move(1, 2)
    h.move(0, 1)
    h.move(0, 2)
    h.move(1, 2)
    assert h._state.tower[2] == 0b1111


def test_move_locked():
    h = Hanoi(4, 0, 2)
    h._lock.acquire()
    with pytest.raises(TimeoutError):
        h.move(0, 2, 0)


def test_move_source_n1():
    h = Hanoi(4, 0, 2)
    with pytest.raises(ValueError, match=r'source -1 is invalid'):
        h.move(-1, 2)


def test_move_source_n1():
    h = Hanoi(4, 0, 2)
    with pytest.raises(ValueError, match=r'source 3 is invalid'):
        h.move(3, 2)


def test_move_target_n1():
    h = Hanoi(4, 0, 2)
    with pytest.raises(ValueError, match=r'target -1 is invalid'):
        h.move(0, -1)


def test_move_target_n1():
    h = Hanoi(4, 0, 2)
    with pytest.raises(ValueError, match=r'target 3 is invalid'):
        h.move(0, 3)


def test_move_source_eq_target():
    h = Hanoi(4, 0, 2)
    with pytest.raises(ValueError, match=r'source may not equal target'):
        h.move(0, 0)


def test_move_empty_source():
    h = Hanoi(4, 0, 2)
    with pytest.raises(ValueError, match=r'source 1 is empty'):
        h.move(1, 0)


def test_move_bigger_disc():
    h = Hanoi(4, 0, 2)
    h.move(0, 2)
    with pytest.raises(ValueError, match=r'cannot put disc 2 on top of disc 1'):
        h.move(0, 2)


def test_isComplete_happy_path():
    h = Hanoi(4, 0, 2)
    assert not h.isComplete()


def test_isComplete_locked():
    h = Hanoi(4, 0, 2)
    h._lock.acquire()
    with pytest.raises(TimeoutError):
        h.isComplete(0)
