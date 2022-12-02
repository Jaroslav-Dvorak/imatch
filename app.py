from flask import Flask
from flask_socketio import SocketIO
from play_sessions import PlaySessions
from secrets import token_hex

app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(16)
socketio = SocketIO(app)
playing = PlaySessions(socketio)
