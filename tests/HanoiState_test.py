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

from hanoi import HanoiState


def test_init_happy_path():
    h = HanoiState(4, 0, 2)
    assert h.numberOfDiscs == 4
    assert h.source == 0
    assert h.target == 2
    assert h.numberOfMoves == 0
    assert h.tower[0] == 0b1111
    assert h.tower[1] == 0b0000
    assert h.tower[2] == 0b0000


def test_init_numberOfDiscs_n1():
    with pytest.raises(ValueError, match=r"numberOfDiscs -1 is invalid"):
        h = HanoiState(-1, 0, 2)


def test_init_numberOfDiscs_gt64():
    with pytest.raises(ValueError, match=r"numberOfDiscs 65 is invalid"):
        h = HanoiState(65, 0, 2)


def test_init_source_n1():
    with pytest.raises(ValueError, match=r"source -1 is invalid"):
        h = HanoiState(1, -1, 2)


def test_init_source_gt2():
    with pytest.raises(ValueError, match=r"source 3 is invalid"):
        h = HanoiState(1, 3, 2)


def test_init_target_n1():
    with pytest.raises(ValueError, match=r"target -1 is invalid"):
        h = HanoiState(1, 0, -1)


def test_init_target_gt2():
    with pytest.raises(ValueError, match=r"target 3 is invalid"):
        h = HanoiState(1, 0, 3)


def test_init_source_eq_target():
    with pytest.raises(ValueError, match=r"source may not equal target"):
        h = HanoiState(1, 0, 0)
