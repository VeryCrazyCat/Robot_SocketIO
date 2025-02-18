#!/usr/bin/python
# run.py

from flask import Flask, render_template,request, redirect, Blueprint, send_from_directory
import api.routes.index as index
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms

import api.sockets.socket_to_server as socket_to_server


import subprocess
from flask import session
import uuid
import time


blueprint = Blueprint('blueprint', __name__, template_folder='../api/templates', static_folder='../api/static')
socketio = SocketIO(debug=True, cors_allowed_origins='*')


@blueprint.route('/', endpoint="index", methods=["GET", "POST"])
def index_():
    return index.load_index()


@blueprint.route('/api/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(blueprint.static_folder, filename)

@blueprint.route('/static/<path:filename>')
def serve_static1(filename): #!THIS IS FOR LOCAL TESTING NAHHHHHGHHHH GOING ON PROD HAHAGHAHAGGHAHAHHAHGAG
    return send_from_directory(blueprint.static_folder, filename)








@socketio.on('socket_to_server')
def on_join(data):
    socket_to_server.on_connect(data)
        
