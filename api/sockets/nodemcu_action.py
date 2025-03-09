from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import flask, uuid
from flask import session, request
import api.routes.emitter as emitter
import ast
def on_connect(data):
    print("received from client")
    emitter.robot_emit(data["action"])
    emit("socket_to_client", {"data": "hello from the server"})

def emit_nodemcu_status(msg):
    print(f"Emitting to all: {msg}")
    emit("nodemcu_status", {"data": str(msg)}, namespace='/',broadcast=True)