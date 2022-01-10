from flask import Flask, render_template, request
import numpy as np
import cv2


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello_world():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html', user_image = '')
    else:
        txt64 = request.form['txt64']
        return render_template('index.html', user_image = '')
