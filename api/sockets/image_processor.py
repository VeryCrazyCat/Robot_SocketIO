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
from torchvision import transforms
import torch
from ultralytics import YOLO

from inference import get_model
import supervision as sv

from api.routes.emitter import calc_rotation
from api.routes.emitter import stop_robot

frames_detected = 0
stop = 0
model = YOLO("model.pt")
#solidwaste-detection/7
#waste-detection-ctmyy/9
#trash-2.0/1
#waste-beverage-bottles/4


def predict(data):
    results = model(data)
    
    for result in results:
        boxes = result.boxes
        
        confs = boxes.conf.cpu().numpy()
        if confs:
            max_index = confs.argmax()

            #x, y, x, y format
            box = boxes.xyxy[max_index][0].cpu().numpy()

            # Calculate the center coordinates
            _center_x = (box[0] + box[2]) / 2
            _center_y = (box[1] + box[3]) / 2
            return _center_x, _center_y
    else:
        return -9999,-9999



def on_connect(data_image):

    image = readb64(data_image)
    center_x, center_y = predict(image)
    
    global frames_detected
    global stop

    if (center_x != -9999):
        cv2.circle(image, (center_x, center_y), 5, (255,255,0), 5)
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

    #return pimg as cv2 array needed for mediapipe
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
