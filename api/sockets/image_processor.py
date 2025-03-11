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
from imageio import imread
import os

from inference import get_model
import supervision as sv

from api.routes.emitter import calc_rotation
from api.routes.emitter import stop_robot
import time
frames_detected = 0
stop = 0
model = get_model(model_id="plastic-recyclable-detection/2", api_key="zNbnK1VDFdmzJG12zJxY")
#solidwaste-detection/7
#waste-detection-ctmyy/9
#trash-2.0/1
#waste-beverage-bottles/4
def on_connect(data_image):
    time_now = time.time()
    image = readb64(data_image)
    segments = split_image(image, 3, 3)
    results = model.infer(image)[0]
    
    global frames_detected
    global stop
    confidence = 0.6
    predicted = False
    center_x, center_y = 0,0
    for obj in list(results.predictions):

        if obj.confidence > confidence:
            confidence = obj.confidence
        
            center_x = int(obj.x)
            center_y = int(obj.y)
            predicted = True

    if predicted:
        cv2.circle(image, (center_x, center_y), 10, (255,255,0), 5)
        print(center_x)
        stop = 0
        frames_detected += 1
        if frames_detected >= 1:
            calc_rotation(center_x)
            frames_detected = 0
    else:
        stop += 1
        if stop >= 5:
            stop_robot()
            stop = 0
            
    
    buffer = io.BytesIO()

    #Converts NP array to image, saves it to io buffer
    Image.fromarray(image).save(buffer, format='JPEG', quality=75)
    encodedString = base64.b64encode(buffer.getbuffer())
    # display the image
    #sv.plot_image(annotated_image)
    emit("annotated_image_output", {"data": str(encodedString.decode("utf-8"))}, namespace='/',broadcast=True)

        

def readb64(base64_string):
    idx = base64_string.find('base64,')
    base64_string  = base64_string[idx+7:]
    image_binary=base64.b64decode(base64_string)
    #return image_binary
    sbuf = io.BytesIO()

    sbuf.write(base64.b64decode(base64_string, ' /'))
    pimg = Image.open(sbuf)
    #return pimg

    array = np.array(pimg)
    return array

def split_image(image, rows, cols):
    height, width = image.shape[:2] #first two elements are width and height
    part_height = height // rows
    part_width = width // cols
    parts = [
        [
            [] for x in range(3)
        ] for y in range(3)
    ]

    for r in range(rows):
        for c in range(cols):
            y_start = r * part_height
            y_end = (r + 1) * part_height

            x_start = c * part_width
            x_end = (c + 1) * part_width

            part = image[y_start:y_end, x_start:x_end]
            parts[c][r] = part
