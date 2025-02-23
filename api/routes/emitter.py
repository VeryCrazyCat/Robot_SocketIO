from flask import Flask, render_template,request, redirect, Blueprint, send_from_directory
import time, json, threading
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

def emit(signal):
    
    emit_queue.put(int(signal))
    print(f"{str(signal)} queued!")