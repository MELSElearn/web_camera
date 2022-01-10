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
        #nparr = np.frombuffer(base64.b64decode(encoded_data), dtype=np.uint8)
        return render_template('index.html', user_image = '')
