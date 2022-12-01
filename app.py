from flask import Flask
from flask_socketio import SocketIO
from play_sessions import PlaySessions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9517009497b59806cb30fd2798171d3'
socketio = SocketIO(app)
playing = PlaySessions(socketio)
