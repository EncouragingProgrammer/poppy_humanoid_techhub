# poppy_motors.py
import platform
import pypot.dynamixel
import random
import threading
import time as t
import serial.tools.list_ports

# Detect OS and set correct port
# -------------------------------
# CONFIG
# -------------------------------

PORT = None
BAUDRATE = 1000000  # 1Mbaud for USB2Dynamixel

if platform.system() == "Windows":
    try:
        test = serial.Serial("COM8", BAUDRATE, timeout=1)
        test.close()
        PORT = "COM8"
        print("Running on Windows – connected to COM8")
    except Exception as e:
        print(f"Running on Windows – could not open COM8 ({e}). Setting PORT = None")
        PORT = None

elif platform.system() == "Linux":
    try:
        test = serial.Serial("/dev/ttyUSB0", BAUDRATE, timeout=1)
        test.close()
        PORT = "/dev/ttyUSB0"
        print("Running on Linux – connected to /dev/ttyUSB0")
    except Exception as e:
        print(f"Running on Linux – could not open /dev/ttyUSB0 ({e}). Setting PORT = None")
        PORT = None

else:
    print("Unsupported OS. Please set the PORT variable manually.")
    PORT = None



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
    """Disable torque on arm motors only."""
    open_connection()
    arm_ids = [51, 52, 53, 54, 41, 42, 43, 44]  # right + left arm
    for m in arm_ids:
        dxl_io._set_torque_enable({m: 0})
        print(f"Arm motor {m} relaxed.")

# -------------------------------
# ANIMATIONS / POSES
# -------------------------------
def wave_poppy(duration=2):
    """Simple wave animation (left arm waves while right arm stays in drive)."""
    reset_stop_flag()
    print("Wave Poppy")

    # Position 1 – left arm up, elbow bent
    step1 = {
        # Left arm
        41: -136,   # L_SHOULDER_Y
        42: -16,    # L_SHOULDER_X
        43: 80,     # L_ARM_Z
        44: -117,   # L_ELBOW_Y

        # Right arm (drive pose)
        51: -170,
        52: -112,
        53: -65,
        54: 135,

        # Torso
        33: -4.26,   # ABS_Z
        34: -10.75,  # BUST_Y
        35: 0.92,    # BUST_X

        # Head
        36: -48,     # HEAD_Z slight turn
        37: -0.44,   # HEAD_Y
    }

    # Position 2 – shift left arm for wave motion
    step2 = {
        # Left arm
        41: -118,   # L_SHOULDER_Y
        42: -12,    # L_SHOULDER_X
        43: 78,     # L_ARM_Z
        44: -160,   # L_ELBOW_Y

        # Right arm (drive pose)
        51: -170,
        52: -112,
        53: -65,
        54: 135,

        # Torso
        33: -4.26,
        34: -10.75,
        35: 0.92,

        # Head
        36: -48,   # same head turn
        37: -0.44,
    }

    # Sequence: step1 → step2 → step1 → step2 → back to drive
    move_motors_timed(step1, duration)
    if stop_flag: return
    move_motors_timed(step2, duration)
    if stop_flag: return
    move_motors_timed(step1, duration)
    if stop_flag: return
    move_motors_timed(step2, duration)
    if stop_flag: return
    t.sleep(0.5)

    # Back to drive
    drive(duration)


def cruise(duration=2):
    """Hands on wheel pose."""
    reset_stop_flag()
    print("Drive pose")

    target_positions = {
        # Right arm
        51: -170,   # R_SHOULDER_Y
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
    """Arms up 'weeee' pose."""
    reset_stop_flag()
    print("Hands up pose")

    target_positions = {
        # Right arm
        51: -80,    # R_SHOULDER_Y
        52: -84,    # R_SHOULDER_X
        53: -87,    # R_ARM_Z
        54: 148,    # R_ELBOW_Y

        # Left arm
        41: -111,   # L_SHOULDER_Y
        42: 15,     # L_SHOULDER_X
        43: 60,     # L_ARM_Z
        44: -118,   # L_ELBOW_Y

        # Torso & head
        33: -4.26,  # ABS_Z
        34: -10.75, # BUST_Y
        35: 0.92,   # BUST_X
        36: -77.57, # HEAD_Z
        37: -0.44,  # HEAD_Y
    }

    move_motors_timed(target_positions, duration)


def drive(duration=2):
    """Neutral driving/cruise pose."""
    reset_stop_flag()
    print("Drive pose")

    target_positions = {
        # Right arm
        51: -170,     # R_SHOULDER_Y
        52: -115,    # R_SHOULDER_X
        53: -65,     # R_ARM_Z
        54: 135,     # R_ELBOW_Y

        # Left arm
        41: -30,   # L_SHOULDER_Y
        42: 36,      # L_SHOULDER_X
        43: 71,      # L_ARM_Z
        44: -106,  # L_ELBOW_Y

        # Torso & head
        33: -4.26,   # ABS_Z
        34: -10.75,  # BUST_Y
        35: 0.92,    # BUST_X
        36: -77.57,  # HEAD_Z
        37: -0.44,   # HEAD_Y
    }

    move_motors_timed(target_positions, duration)


def random_mode(interval=20):
    """Cycle through animations randomly every `interval` seconds."""
    reset_stop_flag()
    print("Random mode started")

    animations = [wave_poppy, cruise, hands_up, drive]

    def loop():
        while not stop_flag:
            anim = random.choice(animations)
            print(f"Random: running {anim.__name__}")
            anim(duration=2)
            for _ in range(interval):
                if stop_flag:
                    print("Random mode stopped")
                    return
                t.sleep(1)

    threading.Thread(target=loop, daemon=True).start()