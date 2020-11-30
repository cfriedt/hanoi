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
