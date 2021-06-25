import flask
from flask import request
import numpy as np
import cv2

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return 'Hello world!'
    if request.method == 'POST':
        img_byte_content = request.form.get('image')
        nparr = np.fromstring(img_byte_content, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        return img_np