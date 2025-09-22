# GCS-SITL

# GCS-SITL

**GCS-SITL** is a web-based Ground Control Station (GCS) interface for controlling and monitoring drones in a Software-In-The-Loop (SITL) simulation environment. It bridges ROS (Robot Operating System) telemetry and commands to a modern Flask web app, providing real-time command, telemetry, and video streaming.

---

## 📺 Demo Video

[![GCS-SITL Demo](https://img.youtube.com/vi/JfEx5KIGv_0/0.jpg)](https://www.youtube.com/watch?v=JfEx5KIGv_0)

---

## Features

- **Web Interface**: Modern, interactive control dashboard (`templates/index.html`).
- **Real-Time Telemetry**: Receives GPS, altitude, state, and battery data from ROS topics.
- **Drone Control**: Supports arming, takeoff, landing, mode switching, and RTL (Return-To-Launch) through web commands.
- **Video Streaming**: Integrates MJPEG video relay with Flask Blueprint.
- **SocketIO Communication**: Bi-directional communication for telemetry and commands via websockets.

## Architecture

- **Flask App (`app.py`)**
  - Serves the web dashboard.
  - Registers the video streaming blueprint.
  - Handles socket events for drone commands (ARM, TAKEOFF, LAND, RTL).
  - Starts a ROS listener thread for incoming telemetry.

- **ROS Bridge (`ros_ws_bridge.py`)**
  - Subscribes to ROS topics: GPS, altitude, state, battery.
  - Emits telemetry and status updates to the Web UI at 1 Hz.
  - Exposes drone control functions (`arm_drone`, `takeoff_drone`, `land_drone`, `set_mode`).

- **Video Relay (`video/relay.py`)**
  - Provides MJPEG video stream endpoint used by the web dashboard.

- **Templates (`templates/index.html`)**
  - Main web UI for control and visualization.
  - Receives telemetry/status via SocketIO and displays real-time data and video.

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/apangireac23/GCS-SITL.git
   cd GCS-SITL
   ```

2. **Install Python dependencies:**
   ```bash
   pip install flask flask-socketio eventlet
   # Plus ROS dependencies (`rospy`, `mavros_msgs`, etc.) via your ROS environment.
   ```

3. **Run the Flask server:**
   ```bash
   python app.py
   ```

4. **Access the dashboard:**
   - Open [http://localhost:5000](http://localhost:5000) in your browser.

5. **Simulate or connect SITL/ROS:**
   - Ensure your ROS environment is running and publishing the required topics.

## File Structure

```
GCS-SITL/
├── app.py                # Main Flask server and SocketIO logic
├── ros_ws_bridge.py      # ROS <-> Websocket bridge, drone control functions
├── templates/
│   └── index.html        # Main web UI template
├── video/
│   └── relay.py          # MJPEG video streaming blueprint
├── README.md
```

## Requirements

- Python 3.x
- Flask, Flask-SocketIO, Eventlet
- ROS (with `rospy`, `mavros_msgs`, `sensor_msgs`)
- SITL (Software-In-The-Loop) drone simulator (e.g., PX4, ArduPilot)

## Usage

- Use the web interface to send ARM, TAKEOFF, LAND, and RTL commands.
- Monitor GPS, altitude, state (armed, connected, mode), and battery voltage in real-time.
- View live MJPEG video feed from the drone simulation.

## License

[MIT](LICENSE)

---

*For full details on usage and customization, see the source code and the main dashboard (`index.html`).*
