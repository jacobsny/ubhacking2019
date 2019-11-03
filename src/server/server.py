
from flask import Flask
from flask_socketio import SocketIO, emit

import base64
import io
import json
import base64


app = Flask(__name__)
app.config['SECRET_KEY'] = "whatamievendoing"
socketio = SocketIO(app)

@socketio.on('toServer')
def handleImage(imgRaw):

    encodedImage = base64.b64encode(imgRaw)

    return encodedImage


def sendImage(encodedImage):

    decodedImage = base64.b64decode(encodedImage)

    return decodedImage





















