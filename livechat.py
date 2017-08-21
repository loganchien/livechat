#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.secret_key = os.urandom(48)
app.debug = True

socketio = SocketIO(app)

_msgs = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send-msg')
def handle_message(msg):
    _msgs.append(msg)
    emit('show-msg', msg, broadcast=True)

@socketio.on('request-all-msgs')
def handle_sync():
    emit('show-all-msgs', _msgs)

if __name__ == '__main__':
    socketio.run(app)
