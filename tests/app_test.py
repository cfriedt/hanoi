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

import pytest
import requests
import json
import logging as log
from multiprocessing import Process
from hanoi import app

# default flask host and port
host = 'localhost'
port = 5000
# connection timeout (s)
timeout = 3
# start server in setup and kill in teardown
server = None


def setup_function(function):
    global server
    log.debug('creating app server..')
    server = Process(target=app.run)
    server.start()
    log.debug('started app server {}'.format(server))


def teardown_function(function):
    global server
    log.debug('sending exception to {}'.format(server))
    server.terminate()
    server.join()
    log.debug('joined server {}'.format(server))
    server = None
    app.sessions = {}


def test_getSessions_none():
    global host
    global port
    global timeout
    r = requests.get(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    assert '{}'.format(r.json()) == '[]'


def test_getSessions_one():
    global host
    global port
    global timeout
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    id = r.json()
    r = requests.get(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    d = r.json()
    assert len(d) == 1
    for e in d:
        e = json.loads(e)
        assert e['sessionId'] == id
        assert e['numberOfDiscs'] == 4
        assert e['fromTower'] == 0
        assert e['toTower'] == 2
        assert e['numberOfMoves'] == 0
        assert e['towers'] == [15, 0, 0]


def test_getSessions_two():
    global host
    global port
    global timeout
    id = {}
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    id[0] = r.json()
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    id[1] = r.json()
    r = requests.get(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    d = r.json()
    assert len(d) == 2
    for i in range(0, len(d)):
        e = json.loads(d[i])
        assert e['sessionId'] == id[i]
        assert e['numberOfDiscs'] == 4
        assert e['fromTower'] == 0
        assert e['toTower'] == 2
        assert e['numberOfMoves'] == 0
        assert e['towers'] == [15, 0, 0]


@pytest.mark.skip(reason="I can't seem to inject garbage data here. It just always wors, dammit!")
def test_getSessions_exception():
    global host
    global port
    global timeout
    import hanoi
    hanoi.app.sessions = 42
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 201


def test_createSession_None_None_None():
    global host
    global port
    global timeout
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200


def test_createSession_8_2_0():
    global host
    global port
    global timeout
    payload = {'numberOfDiscs': '8', 'fromTower': '2', 'toTower': '0'}
    r = requests.post('http://{}:{}/v1/sessions'.format(host,
                                                        port), params=payload, timeout=timeout)
    assert r.status_code == 200
    id = r.json()
    r = requests.get(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    d = r.json()
    assert len(d) == 1
    for e in d:
        e = json.loads(e)
        assert e['sessionId'] == id
        assert e['numberOfDiscs'] == 8
        assert e['fromTower'] == 2
        assert e['toTower'] == 0
        assert e['numberOfMoves'] == 0
        assert e['towers'] == [0, 0, 255]


def test_createSession_exception():
    global host
    global port
    global timeout
    payload = {'numberOfDiscs': 'fleventysix'}
    r = requests.post('http://{}:{}/v1/sessions'.format(host,
                                                        port), params=payload, timeout=timeout)
    # doesn't even make it to my handler - rejected because format is invalid
    assert r.status_code == 400
    payload = {'numberOfDiscs': '-1'}
    r = requests.post('http://{}:{}/v1/sessions'.format(host,
                                                        port), params=payload, timeout=timeout)
    assert r.status_code == 201
    d = json.loads(r.json())
    assert d['code'] == 201
    assert d['message'] != ''


def test_getSession_0():
    global host
    global port
    global timeout
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    id = r.json()
    r = requests.get(
        'http://{}:{}/v1/sessions/{}'.format(host, port, id), timeout=timeout)
    assert r.status_code == 200
    d = json.loads(r.json())
    assert d['sessionId'] == id
    assert d['numberOfDiscs'] == 4
    assert d['fromTower'] == 0
    assert d['toTower'] == 2
    assert d['numberOfMoves'] == 0
    assert d['towers'] == [15, 0, 0]


def test_getSession_exception():
    global host
    global port
    global timeout
    r = requests.get(
        'http://{}:{}/v1/sessions/42'.format(host, port), timeout=timeout)
    assert r.status_code == 201
    d = json.loads(r.json())
    assert d['code'] == 201
    assert d['message'] != ''


def test_getSession_move_0_1():
    global host
    global port
    global timeout
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    id = r.json()
    payload = {'fromTower': '0', 'toTower': '1'}
    r = requests.put('http://{}:{}/v1/sessions/{}/move'.format(host,
                                                               port, id), params=payload, timeout=timeout)
    assert r.status_code == 200


def test_getSession_move_exception():
    global host
    global port
    global timeout
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    id = r.json()
    payload = {'fromTower': '-1', 'toTower': '1'}
    r = requests.put('http://{}:{}/v1/sessions/{}/move'.format(host,
                                                               port, id), params=payload, timeout=timeout)
    assert r.status_code == 201
    d = json.loads(r.json())
    assert d['code'] == 201
    assert d['message'] != ''


def test_getSession_isComplete_false():
    global host
    global port
    global timeout
    r = requests.post(
        'http://{}:{}/v1/sessions'.format(host, port), timeout=timeout)
    assert r.status_code == 200
    id = r.json()
    r = requests.get(
        'http://{}:{}/v1/sessions/{}/complete'.format(host, port, id), timeout=timeout)
    assert r.status_code == 200
    assert '{}'.format(r.json()) == 'False'


def test_getSession_isComplete_exception():
    global host
    global port
    global timeout
    r = requests.put(
        'http://{}:{}/v1/sessions/42/complete'.format(host, port), timeout=timeout)
    # doesn't even get to my handler
    assert r.status_code == 405
