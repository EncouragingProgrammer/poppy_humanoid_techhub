import json
import pypot.dynamixel
import time as t

# Parameters (adjust as needed)
PORT = 'COM8'  # Adjust to your port
BAUDRATE = 1000000  # Adjust to your baudrate

# Motor names and ID numbers.
R_SHOULDER_Y = 51
R_SHOULDER_X = 52
R_ARM_Z = 53
R_ELBOW_Y = 54
L_SHOULDER_Y = 41
L_SHOULDER_X = 42
L_ARM_Z = 43
L_ELBOW_Y = 44
HEAD_Y = 37
HEAD_Z = 36
BUST_X = 35
BUST_Y = 34
ABS_Z = 33

# Motor ID to name mapping
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

def move_motor_timed(motor_id, goal_position, duration):
    # Initialize the DxlIO object
    dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)

    try:
        # Check if the motor is reachable
        if dxl_io.ping(motor_id):
            print(f"Motor {motor_id} is reachable.")

            # Get the current position of the motor
            current_position = dxl_io.get_present_position([motor_id])[0]
            print(f"Current position: {current_position}")

            # Normalize the goal and current positions to the range [-180, 180]
            def normalize_angle(angle):
                while angle > 180:
                    angle -= 360
                while angle < -180:
                    angle += 360
                return angle

            current_position = normalize_angle(current_position)
            goal_position = normalize_angle(goal_position)

            # Calculate the shortest difference between current and goal positions
            diff = goal_position - current_position

            # Handle wraparound by taking the shortest path
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360

            print(f"Moving from {current_position} to {goal_position} with a difference of {diff} degrees")

            # Calculate the number of steps and step duration
            steps = 50  # Number of steps to take between current and goal position
            step_duration = duration / steps  # Time per step
            step_size = diff / steps  # Position change per step

            # Gradually move to the goal position
            for step in range(steps):
                current_position += step_size
                current_position = normalize_angle(current_position)  # Normalize after each step
                dxl_io.set_goal_position({motor_id: current_position})
                t.sleep(step_duration)  # Wait for the duration of the step

            # Ensure the final position is set accurately
            dxl_io.set_goal_position({motor_id: goal_position})
            print(f"Final position set to {goal_position}")

        else:
            print(f"Motor {motor_id} is not reachable.")

    finally:
        # Close the DxlIO object to free the port
        dxl_io.close()


def move_motor_instant(motor_id, goal_position):
    # Initialize the DxlIO object
    dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)
    
    try:
        # Check if the motor is reachable
        if dxl_io.ping(motor_id):
            # Set the goal position for the motor
            dxl_io.set_goal_position({motor_id: goal_position})
            print(f"Motor {motor_id} moved to position {goal_position}.")
        else:
            print(f"Motor {motor_id} is not reachable.")
    
    finally:
        # Close the DxlIO object to free the port
        dxl_io.close()

def move_motors_batch(target_positions, duration):
    # Initialize the DxlIO object
    dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)
    
    try:
        # Check if all motors are reachable
        if all(dxl_io.ping(motor_id) for motor_id in target_positions.keys()):
            print("All motors are reachable.")

            # Calculate the number of steps and step duration
            steps_per_second = 25
            steps = duration * steps_per_second # 5 steps per 
            step_duration = 1 / steps_per_second # Time per step

            # Get the current positions of all motors
            current_positions = dxl_io.get_present_position(list(target_positions.keys()))
            position_changes = {motor_id: (target_positions[motor_id] - current_position) / steps
                                for motor_id, current_position in zip(target_positions.keys(), current_positions)}

            # Gradually move to the goal positions
            for step in range(steps):
                step_positions = {motor_id: current_positions[i] + position_changes[motor_id] * (step + 1)
                                for i, motor_id in enumerate(target_positions.keys())}
                dxl_io.set_goal_position(step_positions)
                t.sleep(step_duration)  # Wait for the duration of the step

            # Ensure all final positions are set accurately
            dxl_io.set_goal_position(target_positions)
            print(f"Final positions set.")

        else:
            print("Some motors are not reachable.")
    except Exception as e:
        print('Error: {}',format(e))


def get_all_motor_positions():
    motor_ids = list(motor_names.keys())
    dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)
    
    try:
        positions = {}
        if all(dxl_io.ping(motor_id) for motor_id in motor_ids):
            all_positions = dxl_io.get_present_position(motor_ids)
            for motor_id, position in zip(motor_ids, all_positions):
                motor_name = motor_names.get(motor_id, 'Unknown Motor')
                positions[motor_name] = position
            
            # Custom formatting without quotes around keys
            formatted_positions = '{\n' + ',\n'.join(f'  {key}: {value}' for key, value in positions.items()) + '\n}'
            print(formatted_positions)
            
            return positions
        else:
            print("Some motors are not reachable.")
            return positions
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


# Function to perform a wave by moving all motors to specified positions over 2 seconds
def start_position(duration):
    # Initialize the positions
    target_positions = {
        R_SHOULDER_Y: 118.64,
        R_SHOULDER_X: -103.52,
        R_ARM_Z: -39.08,
        R_ELBOW_Y: -148.35,
        L_SHOULDER_Y: 48.13,
        L_SHOULDER_X: 23.78,
        L_ARM_Z: 13.41,
        L_ELBOW_Y: 172.0,
        HEAD_Y: -3.96,
        HEAD_Z: -77.27,
        BUST_X: 1.45,
        BUST_Y: -8.22,
        ABS_Z: -4.53
    }

    move_motors_batch(target_positions, duration)

    # Function to perform a wave by moving all motors to specified positions over 2 seconds
def reach_forward(duration):
    # Initialize the positions
    target_positions = {
        R_SHOULDER_Y: -133.05,
        R_SHOULDER_X: -117.23,
        R_ARM_Z: -3.47,
        R_ELBOW_Y: 133.85,
        L_SHOULDER_Y: -65.19,
        L_SHOULDER_X: 37.23,
        L_ARM_Z: -15.78,
        L_ELBOW_Y: -99.38,
        HEAD_Y: -1.61,
        HEAD_Z: -89.88,
        BUST_X: -2.42,
        BUST_Y: -72.31,
        ABS_Z: -6.99
    }

    move_motors_batch(target_positions, duration)


def record_motor_positions(frequency, duration, filename):
    start_time = t.time()
    end_time = start_time + duration
    recordings = []

    while t.time() < end_time:
        positions = get_all_motor_positions()
        if positions:
            # Append the positions dictionary directly to the recordings list
            recordings.append(positions)
            # Print the current recording
            positions_json = json.dumps(positions, indent=2)
            print(f"Recording: {positions_json}")
        t.sleep(frequency)

    # Save recordings to a file in JSON array format
    with open(filename, 'w') as file:
        # Convert the list of recordings to JSON format and write to the file
        json.dump(recordings, file, indent=2)

    print(f"Recordings saved to {filename}.")


def play_recordings(filename, duration_per_position):
    # Load the recordings from the file
    with open(filename, 'r') as file:
        recordings = json.load(file)
    
    # Playback each recording
    for positions in recordings:
        # Print current positions for debugging
        print(f"Moving to positions: {positions}")
        
        # Convert motor names to IDs for moving motors
        positions_ids = {motor_names_rev[motor]: pos for motor, pos in positions.items() if motor in motor_names_rev}
        
        # Move motors to the desired positions
        move_motors_batch(positions_ids, duration_per_position)
        t.sleep(1)  # Optional: Pause between each recording playback

    print("Playback complete.")

# Reverse the motor_names dictionary for lookup
motor_names_rev = {v: k for k, v in motor_names.items()}

relax_motors(list(motor_names.keys()))

get_all_motor_positions()

start_position(2)

t.sleep(5)

reach_forward(2)

# relax_motors(list(motor_names.keys()))

t.sleep(5)

positon_recording_file_name = 'position_recordings/wave_1.json'
frequency = 0.3

# # Example usage
# record_motor_positions(frequency, 12, positon_recording_file_name)

# Example usage
# play_recordings(positon_recording_file_name, frequency)

# start_position(3)

# relax_motors(list(motor_names.keys()))