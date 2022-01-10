from flask import Flask, render_template, request
from PIL import Image
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
        img64 = request.form['base64']
        encoded_data = img64.split(',')[1]
        return render_template('index.html', user_image = encoded_data)
