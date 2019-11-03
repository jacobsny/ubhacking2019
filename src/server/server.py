
from flask import Flask
from flask_socketio import SocketIO, emit, send

import base64


app = Flask(__name__)
app.config['SECRET_KEY'] = "whatamievendoing"
socketio = SocketIO(app)

@socketio.on('imageHandler')
def handleImage(imgRaw):

    encodedImage = base64.b64encode(imgRaw)

    encodedOverlay = jacobCode(encodedImage)

    overlay = base64.b64decode(encodedOverlay)

    socketio.send(overlay)


if __name__ == "__main__":
    socketio.run(app, debug=True)




















