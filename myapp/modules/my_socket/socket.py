# -*- coding: UTF-8 -*-
from flask import Flask, render_template, Blueprint, jsonify, request, current_app
from flask_socketio import SocketIO, emit, join_room, disconnect
import time
from myapp import socketio
from threading import Thread

app = current_app

socket_blu = Blueprint('socket_blu', __name__, template_folder='../templates')

thread = None


def background_stuff():
    """ Let's do it a bit cleaner """
    while True:
        time.sleep(1)
        t = str(time.clock())
        socketio.emit(
            'message', {'data': 'This is data', 'time': t}, namespace='/test')


@socket_blu.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_stuff)
        thread.start()
    return render_template('index.html')


@socketio.on('my event', namespace='/test')
def my_event(msg):
    print('my_event..', msg['data'])


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
