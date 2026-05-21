# pyrefly: ignore [missing-import]
from flask import Flask
# pyrefly: ignore [missing-import]
from flask_socketio import SocketIO
# pyrefly: ignore [missing-import]
from pymongo import MongoClient
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

# MongoDB connection
client = MongoClient(app.config['MONGO_URI'])
try:
    # Verify the connection
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    print("Please ensure MongoDB is installed and running on port 27017.")

db = client.get_database()

def get_db():
    return db

# Register blueprints
from routes.auth import auth_bp
from routes.room import room_bp
app.register_blueprint(auth_bp)
app.register_blueprint(room_bp)

# Register socket events
from sockets.room_events import register_room_events
from sockets.whiteboard_events import register_whiteboard_events
from sockets.pdf_events import register_pdf_events
from sockets.audio_events import register_audio_events

register_room_events(socketio, db)
register_whiteboard_events(socketio, db)
register_pdf_events(socketio, db)
register_audio_events(socketio, db)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    print("=" * 60)
    print("  Adaptive Vector-Based Collaboration System")
    print("  Trincomalee Campus, Eastern University, Sri Lanka")
    print("  Running on http://localhost:5000")
    print("=" * 60)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
