#!/usr/bin/env python

from flask import Flask, render_template, g
from flask_socketio import SocketIO, emit
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(48)
app.debug = True

socketio = SocketIO(app)

DATABASE = 'livechat.sqlite'

def _connect_db():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = _connect_db()
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        with app.open_resource('schema.sql', mode='r') as f:
            db = get_db()
            db.cursor().executescript(f.read())
            db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send-msg')
def handle_message(msg):
    db = get_db()
    db.cursor().execute('INSERT INTO livechat(text) VALUES (?);', (msg,))
    db.commit()
    emit('show-msg', msg, broadcast=True)

@socketio.on('request-all-msgs')
def handle_sync():
    cursor = get_db().cursor()
    cursor.execute('SELECT text FROM livechat ORDER BY id ASC;');
    emit('show-all-msgs', list(cursor.fetchall()))

if __name__ == '__main__':
    socketio.run(app)
