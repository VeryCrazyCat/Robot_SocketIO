from flask import Flask, render_template,request, redirect, Blueprint, send_from_directory
import time, json, threading
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
from queue import Queue

emit_queue = Queue()
def generate():
    while True:
        actions = []
        while not emit_queue.empty():
            actions.append(emit_queue.get())
        data = {
            "value": time.time(),
            "actions": actions
        }
        yield f"data: {json.dumps(data)}\n\n"

        time.sleep(0.005)  # Adjust sleep for update frequency

def robot_emit(signal):
    
    emit_queue.put(int(signal))
    print(f"{str(signal)} queued!")

def calc_rotation(x):
    if x < 290:
        direction = "right"
    if x > 350:
        direction = "left"
    elif 290 <= x <= 350:
        direction = "forward"
    signal = ""
    if direction == "left" or direction == "right":
        amplitude = int(abs(320 - x)/7) #abs allows both left and right rotation
        if amplitude < 0:
            amplitude = 0 #Motor deactivates lower than 30, allows leeway
        
        if direction == "left":
            motor = 0 #left motor
        else:
            motor = 1 #right motor
        
        amplitude += 1040 # at 1040 motor spins slowest without stopping

        signal = f"2{str(motor)}{str(amplitude)}"
        robot_emit(signal)
        emit("image_data_return", {"data": str(signal)}, namespace='/',broadcast=True)
    elif direction == "forward":
        amplitude = 50
        robot_emit(f"20{1040 + amplitude}")
        robot_emit(f"21{1040 + amplitude}")
        emit("image_data_return", {"data": str(f"21{1040 + amplitude}")}, namespace='/',broadcast=True)
    

def stop_robot():
    robot_emit("201000")
    robot_emit("211000")
    emit("image_data_return", {"data": str(211000)}, namespace='/',broadcast=True)