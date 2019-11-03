
from flask import Flask
from flask_socketio import SocketIO, emit
from PIL import Image, ImageDraw

import base64
import io
import json
import base64


#app = Flask(__name__)
#app.config['SECRET_KEY'] = "whatamievendoing"
#socketio = SocketIO(app)

#@socketio.on('toServer')
def handleImage(imgRaw):

    x = base64.b64decode(imgRaw)
    stream = io.BytesIO(x)
    image = Image.open(stream)
    image.save("test.png", "PNG")

with open("download.jpg","rb") as img:
    x = img.read()
    y = base64.b64encode(x)
    handleImage(y)



















