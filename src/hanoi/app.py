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

import logging
from threading import Lock
import connexion
from connexion import NoContent

import hanoi

sessions = {}


def error(code, e):
    message = '{}'.format(e)
    s = ''
    s += '{'
    s += '"code": {}'.format(code) + ', '
    s += '"message": "{}"'.format(message)
    s += '}'
    return s


def getSessions():
    try:
        return [i.getState().to_json() for i in sessions.values()]
    except Exception as e:
        return error(201, e), 201


def createSession(numberOfDiscs=4, fromTower=0, toTower=2):
    try:
        h = hanoi.Hanoi(numberOfDiscs, fromTower, toTower)
        sessions[h._state.id] = h
        return h._state.id
    except Exception as e:
        return error(201, e), 201


def getSession(sessionId):
    try:
        return sessions[sessionId].getState().to_json()
    except Exception as e:
        return error(201, e), 201


def move(sessionId, fromTower, toTower):
    try:
        sessions[sessionId].move(fromTower, toTower)
        return NoContent, 200
    except Exception as e:
        return error(201, e), 201


def isComplete(sessionId):
    try:
        return sessions[sessionId].isComplete()
    except Exception as e:
        return error(201, e), 201


app = connexion.App(__name__)
app.add_api('hanoi.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :$PORT -w hanoi.app
application = app.app
