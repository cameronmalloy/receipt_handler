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
from io import BytesIO

buffered = BytesIO()
Image.fromarray(result).save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue())

app = flask.Flask(__name__)

DEFAULT_OFFSET = 20

def bw_scanner(image, offset):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset = offset, method = "gaussian")
    return (gray > T).astype("uint8") * 255

def decode_img_to_nparr(encoded_img):
    print('Decodinng Image')
    img_byte_content = base64.b64decode(encoded_img)
    print('Converting to np array')
    nparr = np.fromstring(img_byte_content, np.uint8)
    print(len(nparr))
    image_arr = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
    return image_arr

def encode_img(image_arr):
    print('Encoding image array of length', len(image_arr))
    image = Image.fromarray(image_arr)
    buffered = BytesIO()
    image.save(buffered, format='JPEG')
    img_str = base64.bb64encode(buffered.getvalue())
    return img_str

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return 'Hello world!'
    if request.method == 'POST':
        # Get encoded post form
        print(request.form.keys())
        request_type = request.form.get('type')
        encoded_img = request.form.get('image')
        if request_type == 'bw':
            offset = request.form.get('offset')
            if not offset:
                offset = DEFAULT_OFFSET
            bw_arr = get_offset_img(encoded_img, offset)
            encoded_bw_img = encoded_img(bw_arr)
            return json.dumps({'image': encoded_bw_img})
        elif request_type == 'tesseract':
            image_arr = decode_img_to_nparr(encoded_img)
            try:
                print('doing pytesseract')
                text = pytesseract.image_to_string(Image.fromarray(image_arr))
            except e:
                print(e)
            print(text)
            data = re.findall(r'(.*) (.*[\.,] ?\d{1,2})[^\d]|(.*) (\d+)$', text)
            print(data)
            ret = {'data': []}
            for (name1, price1, name2, price2) in data:
                if price1:
                    data_value = {name1: price1}
                    ret['data'].append(data_value)
                else:
                    data_value = {name2: price2}
                    ret['data'].append(data_value)
            print(ret)
            return json.dumps(ret)

def get_offset_img(encoded_img, offset):
    image_arr = decode_img_to_nparr(encoded_img)
    result_arr = bw_scanner(image_arr, offset)
    return result_arr
    
