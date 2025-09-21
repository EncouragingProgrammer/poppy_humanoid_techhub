# poppy_motors.py
import pypot.dynamixel
import time as t
import platform

# -------------------------------
# CONFIG
# -------------------------------
# Update this if your USB adapter shows up as ttyUSB1 instead

# Detect OS and set correct port
if platform.system() == "Windows":
    # Update this to match the COM port of your USB2Dynamixel adapter
    PORT = "COM8"
    print("Running on Windows")
elif platform.system() == "Linux":
    # On Raspberry Pi / Ubuntu it usually shows up as /dev/ttyUSB0
    PORT = "/dev/ttyUSB0"
    print("Running on Linux")
else:
    print("Unsupported OS. Please set the PORT variable manually.")
    # Get user input for PORT
    PORT = input("Enter the port for your USB2Dynamixel adapter (e.g. /dev/ttyUSB0 or COM3): ")
    print(f"Using port: {PORT}")

BAUDRATE = 1000000

# Motor ID to name mapping (adjust if yours differ)
motor_names = {
    51: 'R_SHOULDER_Y',
    52: 'R_SHOULDER_X',
    53: 'R_ARM_Z',
    54: 'R_ELBOW_Y',
    41: 'L_SHOULDER_Y',
    42: 'L_SHOULDER_X',
    43: 'L_ARM_Z',
    44: 'L_ELBOW_Y',
    37: 'HEAD_Y',
    36: 'HEAD_Z',
    35: 'BUST_X',
    34: 'BUST_Y',
    33: 'ABS_Z'
}

# -------------------------------
# STOP FLAG
# -------------------------------
stop_flag = False

def stop_motion():
    """Interrupts any running movement."""
    global stop_flag
    stop_flag = True
    print("STOP called!")

def reset_stop_flag():
    global stop_flag
    stop_flag = False

# -------------------------------
# CONNECTION
# -------------------------------

dxl_io = None  # global handle

def open_connection():
    global dxl_io
    if dxl_io is None:
        dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)
        print("DxlIO connection opened.")

def close_connection():
    global dxl_io
    if dxl_io is not None:
        dxl_io.close()
        dxl_io = None
        print("DxlIO connection closed.")

# -------------------------------
# MOTOR HELPERS
# -------------------------------
def move_motor_instant(motor_id, goal_position):
    open_connection()
    if dxl_io.ping(motor_id):
        dxl_io.set_goal_position({motor_id: float(goal_position)})
        print(f"Motor {motor_id} moved to {goal_position}.")
    else:
        print(f"Motor {motor_id} is not reachable.")

def move_motors_timed(target_positions, duration):
    """Moves motors smoothly to target positions over 'duration' seconds."""
    open_connection()
    reachable = [m for m in target_positions if dxl_io.ping(m)]
    if not reachable:
        print("No motors reachable.")
        return

    current_positions = dxl_io.get_present_position(reachable)
    steps = 50
    step_time = duration / steps

    for step in range(steps):
        if stop_flag:
            print("Movement stopped early.")
            break

        new_positions = {}
        for i, motor_id in enumerate(reachable):
            current = current_positions[i]
            goal = target_positions[motor_id]
            diff = goal - current

            # Normalize diff into -180..180
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360

            new_positions[motor_id] = current + diff * (step + 1) / steps

        dxl_io.set_goal_position(new_positions)
        t.sleep(step_time)

    print("Movement finished.")


def get_all_motor_positions():
    open_connection()
    positions = {}
    reachable = [m for m in motor_names.keys() if dxl_io.ping(m)]
    if reachable:
        all_positions = dxl_io.get_present_position(reachable)
        for motor_id, position in zip(reachable, all_positions):
            motor_name = motor_names.get(motor_id, f"Motor{motor_id}")
            positions[motor_name] = position
    else:
        print("No motors reachable.")
    return positions


def get_motor_position(motor_id):
    open_connection()
    if dxl_io.ping(motor_id):
        position = dxl_io.get_present_position([motor_id])[0]
        motor_name = motor_names.get(motor_id, f"Motor{motor_id}")
        print(f"{motor_name} (ID: {motor_id}) is at {position:.2f}")
        return position
    else:
        print(f"Motor {motor_id} is not reachable.")
        return None


def relax_motors(motor_ids):
    open_connection()
    for motor_id in motor_ids:
        dxl_io._set_torque_enable({motor_id: 0})
        print(f"Torque of motor {motor_id} disabled.")


def relax_all_motors():
    relax_motors(motor_names.keys())

def relax_arms():
    motor_names = {
        51: 'R_SHOULDER_Y',
        52: 'R_SHOULDER_X',
        53: 'R_ARM_Z',
        54: 'R_ELBOW_Y',
        41: 'L_SHOULDER_Y',
        42: 'L_SHOULDER_X',
        43: 'L_ARM_Z',
        44: 'L_ELBOW_Y',
    }
    relax_motors(motor_names.keys())

# -------------------------------
# ANIMATIONS / POSES
# -------------------------------
def wave_poppy(duration=2):
    """Wave animation (placeholder)."""
    reset_stop_flag()
    print("Wave Poppy (TODO: fill motor positions)")

    # Example structure
    step1 = {
        # TODO: add motor positions for wave start
        # 51: 120.0,
        # 41: -40.0,
    }
    move_motors_timed(step1, duration)

def drive_pose(duration=2):
    """Hands on wheel pose."""
    reset_stop_flag()
    print("Drive pose")

    target_positions = {
        # Right arm
        51: -175,   # R_SHOULDER_Y
        52: -122,   # R_SHOULDER_X
        53: -82,    # R_ARM_Z
        54: 150,    # R_ELBOW_Y

        # Left arm
        41: -9,     # L_SHOULDER_Y
        42: -40,    # L_SHOULDER_X
        43: 59,     # L_ARM_Z
        44: 170,    # L_ELBOW_Y

        # Torso & head
        33: -4.26,  # ABS_Z
        34: -10.75, # BUST_Y
        35: 0.92,   # BUST_X
        36: -77.57, # HEAD_Z
        37: -0.44,  # HEAD_Y
    }

    move_motors_timed(target_positions, duration)


def hands_up(duration=2):
    """Arms up 'weeee' pose (placeholder)."""
    reset_stop_flag()
    print("Hands up pose (TODO: fill motor positions)")

    target_positions = {
        # TODO: add motor positions for hands up
    }
    move_motors_timed(target_positions, duration)

def rest_pose(duration=2):
    """Neutral/rest pose (placeholder)."""
    reset_stop_flag()
    print("Rest pose (TODO: fill motor positions)")

    target_positions = {
        # TODO: add motor positions for relaxed state
    }
    move_motors_timed(target_positions, duration)
    relax_arms()
