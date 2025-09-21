# poppy_motors.py
import pypot.dynamixel
import time as t

# -------------------------------
# CONFIG
# -------------------------------
# Update this if your USB adapter shows up as ttyUSB1 instead
PORT = '/dev/ttyUSB0'
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
# MOTOR HELPERS
# -------------------------------
def move_motors_timed(target_positions, duration):
    """Moves motors smoothly to target positions over 'duration' seconds."""
    dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)
    try:
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
    finally:
        dxl_io.close()

def relax_motors(motor_ids):
    # Initialize the DxlIO object
    dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)
    
    try:
        # Disable torque for each motor
        for motor_id in motor_ids:
            dxl_io._set_torque_enable({motor_id: 0})
            print(f"Torque of motor {motor_id} disabled.")
    finally:
        # Close the DxlIO object to free the port
        dxl_io.close()

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
