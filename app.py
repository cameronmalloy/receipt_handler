import flask
from flask import request
import numpy as np
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import pytesseract
import base64
from skimage.filters import threshold_local
import json
import re

app = flask.Flask(__name__)

DEFAULT_OFFSET = 20

def bw_scanner(image, offset):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset = offset, method = "gaussian")
    return (gray > T).astype("uint8") * 255

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return 'Hello world!'
    if request.method == 'POST':
        # Get encoded post form
        print(request.form)
        encoded_img = request.form.get('image')
        offset = request.form.get('offset')
        if not offset:
            offset = DEFAULT_OFFSET
        print('Byte content type:', type(encoded_img))
        img_byte_content = base64.b64decode(encoded_img)
        print('Decoded content type:', type(img_byte_content))
        nparr = np.fromstring(img_byte_content, np.uint8)
        print(len(nparr))
        image = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        result = bw_scanner(image, offset)
        print(len(result))
        try:
            print('doing pytesseract')
            text = pytesseract.image_to_string(Image.fromarray(result))
        except e:
            print(e)
        print(text)
        data = re.findall(r'(.*) (.*[\.,] ?\d{1,2})[^\d]|(.*) (\d+)$', text)
        print(data)
        ret = {'data': []}
        for name, price in data:
            data_value = {name: price}
            ret['data'].append(data_value)
        print(ret)
        return json.dumps(ret)
