from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import flask, uuid
from flask import session, request
import io
from PIL import Image
import base64,cv2
import imutils
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
model_dir = os.path.abspath("efficientdet_lite0.tflite")
BaseOptions = mp.tasks.BaseOptions
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path='/path/to/model.tflite'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    max_results=5,
)


def on_connect(data_image):
    print("received image from client: " + data_image)
    emit("socket_to_client", {"data": "hello from the server"})
    with ObjectDetector.create_from_options(options) as detector:
        image = mp.Image.create_from_file(readb64(data_image))
        detection_result = detector.detect(image)
        print(detection_result)
        

def readb64(base64_string):
    idx = base64_string.find('base64,')
    base64_string  = base64_string[idx+7:]
    image_binary=base64.decodestring(base64_string)
    return image_binary
    #sbuf = io.BytesIO()

    #sbuf.write(base64.b64decode(base64_string, ' /'))
    #pimg = Image.open(sbuf)

    #return pimg as cv2 array needed for mediapipe
    #return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)