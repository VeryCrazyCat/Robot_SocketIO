from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import flask, uuid
from flask import session, request
def on_connect(data):
    emit("socket_to_client", {"data": "hello from the server"})