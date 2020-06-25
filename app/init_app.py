from app.main import create_app
from flask_socketio import SocketIO, send, join_room
from app.main.config import env


app = create_app(env or 'dev')
socketIo = SocketIO(app, cors_allowed_origins="*")