import os

from app.main import create_app
from flask_socketio import SocketIO, send

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
socketIo = SocketIO(app, cors_allowed_origins="*")