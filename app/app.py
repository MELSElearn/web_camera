from flask import Flask, render_template, request
import numpy as np
import cv2
from base64 import b64decode, b64encode
from cvzone.HandTrackingModule import HandDetector

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello_world():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html', user_image = '')
    else:
        txt64 = request.form['txt64']
        encoded_data = txt64.split(',')[1]
        encoded_data = b64decode(encoded_data)
        nparr = np.frombuffer(encoded_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        detector = HandDetector(detectionCon=0.8, maxHands=2)
        hands, img = detector.findHands(img)
        totalfingers=0
        if hands:
            fingers = detector.fingersUp(hands[0])
            totalfingers = fingers.count(1)
        
        cv2.putText(img,f'{int(totalfingers)}',(50,70), cv2.FONT_HERSHEY_PLAIN,5,(250,0,0),5)
            
        _, im_arr = cv2.imencode('.png', img)
        im_bytes = im_arr.tobytes()
        im_b64 = b64encode(im_bytes).decode("utf-8")

        return render_template('index.html', user_image = im_b64)
    
@app.route('/api/info', methods=['GET','POST'])
def api_info():
    txt64 = request.args.get("todo")
    encoded_data = txt64.split(',')[1]
    encoded_data = b64decode(encoded_data)
    nparr = np.frombuffer(encoded_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    hands, img = detector.findHands(img)
    totalfingers=0
    if hands:
        fingers = detector.fingersUp(hands[0])
        totalfingers = fingers.count(1)
    cv2.putText(img,f'{int(totalfingers)}',(50,70), cv2.FONT_HERSHEY_PLAIN,5,(250,0,0),5)
    _, im_arr = cv2.imencode('.png', img)
    im_bytes = im_arr.tobytes()
    im_b64 = b64encode(im_bytes).decode("utf-8")
    return im_b64
