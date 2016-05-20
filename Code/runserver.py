#!/usr/bin/env python
"""
This script runs the FlaskWebProject1 application using a development server.
"""
from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
#from flask import Flask, render_template, session, request
from flask import  render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from FlaskWebProject1 import app
import sensor
#app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='gevent')
thread = None

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    airquality = 0
    temperature = 0
    fahrenheit = 0
    while True:
        time.sleep(5)
        print("Hello World")
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')
        airquality = sensor.AirRead()
        temperature,fahrenheit = sensor.TemperatureRead()
        print(airquality)
        socketio.emit('my data',
                      {'data': temperature,'data1': fahrenheit,'data2': airquality, },
                      namespace='/test')
        #socketio.emit('my data',
        #              {'Temperature': 10, 'Fahrenheit': 10,'AirQuality': 30,},
        #              namespace='/test')

@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my relay', namespace='/test')
def deal_relay(message):
    print("Recive the button info.")
    if message['data'] == "Open":
        sensor.ControlRelay(1)
        print("Open the relay")
    if message['data'] == "Close":
        sensor.ControlRelay(0)
        print("Close the relay")

@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)




if __name__ == '__main__':
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    socketio.run(app,'0.0.0.0',8000, debug=True)