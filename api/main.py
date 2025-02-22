#!/usr/bin/python
# run.py

from flask import Flask, render_template,request, redirect, Blueprint, send_from_directory, Response, jsonify

import api.routes.camera as camera
import api.routes.index as index
import api.routes.emitter as emitter

from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms

import api.sockets.nodemcu_action as nodemcu_action
import api.sockets.image_processor as image_processor


import subprocess
from flask import session
import uuid
import time, json


blueprint = Blueprint('blueprint', __name__, template_folder='../api/templates', static_folder='../api/static')
socketio = SocketIO(debug=True, cors_allowed_origins='*')
emit_on_next = []



@blueprint.route('/sse')
def sse():
    return Response(emitter.generate(), mimetype='text/event-stream',headers={'Cache-Control': 'no-cache'})

@blueprint.route('/', endpoint="index", methods=["GET", "POST"])
def _index():
    return index.load_index()
    

    

@blueprint.route('/camera', endpoint="camera", methods=["GET", "POST"])
def _camera():
    return camera.load_camera_page()


@blueprint.route('/api/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(blueprint.static_folder, filename)

@blueprint.route('/static/<path:filename>')
def serve_static1(filename):
    return send_from_directory(blueprint.static_folder, filename)

@blueprint.route('/stream', endpoint="stream", methods=["GET", "POST"])
def stream():
    pass



@socketio.on('')
def on_join(data):
    print("received from client")


@socketio.on('nodemcu_action')
def on_join(data):
    nodemcu_action.on_connect(data)
        
@socketio.on('socket_to_image_processor')
def on_join(data):
    image_processor.on_connect(data)
        
