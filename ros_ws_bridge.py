import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64
import threading
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from mavros_msgs.msg import State
import time  # ✅ For timestamping
from sensor_msgs.msg import BatteryState

socketio = None

# Timestamps for rate limiting
last_gps_emit = 0
last_alt_emit = 0
last_state_emit = 0

# Interval in seconds
EMIT_INTERVAL = 1.0  # 1 Hz

def start_ros_listener(socket):
    global socketio
    socketio = socket

    thread = threading.Thread(target=ros_thread)
    thread.daemon = True
    thread.start()

def ros_thread():
    rospy.init_node('telemetry_bridge', anonymous=True)

    rospy.Subscriber("/mavros/global_position/global", NavSatFix, handle_gps)
    rospy.Subscriber("/mavros/global_position/rel_alt", Float64, handle_altitude)
    rospy.Subscriber("/mavros/state", State, handle_state)
    rospy.Subscriber("/mavros/battery", BatteryState, handle_battery)


    print("[ROS] ROS Node started. Subscribed to GPS, Altitude, and State topics.")
    rospy.spin()

def handle_gps(msg):
    global last_gps_emit
    now = time.time()
    if now - last_gps_emit >= EMIT_INTERVAL:
        last_gps_emit = now
        data = {
            "latitude": msg.latitude,
            "longitude": msg.longitude
        }
        if socketio:
            socketio.emit("telemetry", data)
            print("[ROS] Emitting GPS:", data)

def handle_altitude(msg):
    global last_alt_emit
    now = time.time()
    if now - last_alt_emit >= EMIT_INTERVAL:
        last_alt_emit = now
        data = {
            "altitude": msg.data
        }
        if socketio:
            socketio.emit("telemetry", data)
            print("[ROS] Emitting Altitude:", data)

def handle_state(msg):
    global last_state_emit
    now = time.time()
    if now - last_state_emit >= EMIT_INTERVAL:
        last_state_emit = now
        data = {
            "armed": msg.armed,
            "connected": msg.connected,
            "mode": msg.mode
        }
        if socketio:
            socketio.emit("status", data)
            print("[ROS] Emitting State:", data)

def handle_battery(msg):
    data = {"battery_voltage": msg.voltage}
    if socketio:
        socketio.emit("telemetry", data)
        print("[ROS] Emitting Battery Voltage:", data)


def arm_drone():
    rospy.wait_for_service("/mavros/cmd/arming")
    try:
        arm_service = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
        arm_service(True)
        print("[ROS] Drone armed.")
    except rospy.ServiceException as e:
        print("[ERROR] Arming failed:", e)

def takeoff_drone(alt=10):
    rospy.wait_for_service("/mavros/cmd/takeoff")
    try:
        takeoff = rospy.ServiceProxy("/mavros/cmd/takeoff", CommandTOL)
        takeoff(0, 0, 0, 0, alt)
        print(f"[ROS] Takeoff initiated to {alt} meters.")
    except rospy.ServiceException as e:
        print("[ERROR] Takeoff failed:", e)

def land_drone():
    rospy.wait_for_service("/mavros/cmd/land")
    try:
        land = rospy.ServiceProxy("/mavros/cmd/land", CommandTOL)
        land(0, 0, 0, 0, 0)
        print("[ROS] Landing command sent.")
    except rospy.ServiceException as e:
        print("[ERROR] Landing failed:", e)

def set_mode(mode):
    rospy.wait_for_service("/mavros/set_mode")
    try:
        mode_service = rospy.ServiceProxy("/mavros/set_mode", SetMode)
        mode_service(0, mode)
        print(f"[ROS] Mode set to {mode}")
    except rospy.ServiceException as e:
        print(f"[ERROR] Failed to set mode {mode}:", e)
