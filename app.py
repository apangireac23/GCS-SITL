# app.py

import eventlet
eventlet.monkey_patch()  # Needed for Flask-SocketIO to work properly

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import emit

# ROS telemetry and control functions
from ros_ws_bridge import start_ros_listener
from ros_ws_bridge import arm_drone, takeoff_drone, land_drone, set_mode

# Register MJPEG video streaming route
from video.relay import video_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ros-secret'

# Initialize SocketIO with CORS
socketio = SocketIO(app, cors_allowed_origins="*")

# Register the MJPEG video blueprint
app.register_blueprint(video_bp)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("command")
def handle_command(data):
    cmd = data.get("action")
    print(f"[CMD] Received command: {cmd}")

    if cmd == "ARM":
        arm_drone()
    elif cmd == "TAKEOFF":
        set_mode("GUIDED")
        arm_drone()
        takeoff_drone(alt=10)
    elif cmd == "LAND":
        set_mode("LAND")
        land_drone()
    elif cmd == "RTL":
        set_mode("RTL")

if __name__ == "__main__":
    print("[INFO] Starting ROS listener thread...")
    start_ros_listener(socketio)
    print("[INFO] Starting Flask server...")
    socketio.run(app, host="0.0.0.0", port=5000)
