from flask import Flask, render_template, request
import numpy as np
import cv2
from base64 import b64decode, b64encode

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello_world():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html', user_image = '')
    else:
        txt64 = request.form['txt64']
        encoded_data = txt64.split(',')[1]
        nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        _, im_arr = cv2.imencode('.png', img_gray)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = b64encode(im_bytes).decode("utf-8")

        return render_template('index.html', user_image = encoded_data)
