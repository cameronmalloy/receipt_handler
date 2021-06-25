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
        print('posting')
        img_byte_content = request.form.get('image')
        print('Byte content type:', type(img_byte_content))
        print(img_byte_content)
        nparr = np.fromstring(img_byte_content, np.uint8)
        print(len(nparr))
        img_np = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        return str(img_np)
