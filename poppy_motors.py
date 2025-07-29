import json
import pypot.dynamixel
import time as t

stop_flag = False

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



def stop_motion():
    global stop_flag
    stop_flag = True

def reset_stop_flag():
    global stop_flag
    stop_flag = False

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

# def move_motors_timed(target_positions, duration):
#     # Initialize the DxlIO object
#     dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)

#     try:
#         # Check if all motors are reachable
#         reachable_motors = [motor_id for motor_id in target_positions if dxl_io.ping(motor_id)]
#         if not reachable_motors:
#             print("No motors are reachable.")
#             return

#         # Get the current positions of all motors
#         current_positions = dxl_io.get_present_position(reachable_motors)

#         # Define the number of steps and delay between them
#         steps = 50  # Number of steps for smooth movement
#         step_duration = duration / steps  # Time for each step

#         # Gradually move each motor to its goal position
#         for step in range(steps):
#             new_positions = {}
#             for i, motor_id in enumerate(reachable_motors):
#                 current_position = current_positions[i]
#                 goal_position = target_positions[motor_id]
                
#                 # Calculate the incremental step for this motor
#                 # TODO - This section needs some additional logic to prevent the -180 / 180 error. 
#                 # Potentially "flipping" the negative numbers to 360 -> 180, and then converting numbers above 180 back to negatives when giving the "new" position.
#                 position_step = (goal_position - current_position) / steps
                
#                 # Update the motor's position for this step
#                 new_positions[motor_id] = current_position + position_step * (step + 1)
            
#             # Set new goal positions for all motors
#             dxl_io.set_goal_position(new_positions)
            
#             # Wait for the step duration
#             t.sleep(step_duration)

#         print(f"All motors moved to their target positions over {duration} seconds.")
    
#     finally:
#         # Close the DxlIO object to free the port
#         dxl_io.close()

def move_motors_timed(target_positions, duration):
    # Initialize the DxlIO object
    dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)

    try:
        # Check if all motors are reachable
        reachable_motors = [motor_id for motor_id in target_positions if dxl_io.ping(motor_id)]
        if not reachable_motors:
            print("No motors are reachable.")
            return

        # Get the current positions of all motors
        current_positions = dxl_io.get_present_position(reachable_motors)

        # Define the number of steps and delay between them
        steps = 50  # Number of steps for smooth movement
        step_duration = duration / steps  # Time for each step

        # Gradually move each motor to its goal position
        for step in range(steps):
            new_positions = {}
            for i, motor_id in enumerate(reachable_motors):
                current_position = current_positions[i]
                goal_position = target_positions[motor_id]

                # Calculate the difference and normalize within the -180 to 180 range
                diff = goal_position - current_position

                # Adjust for the shortest path considering wrap-around boundary
                if diff > 180:
                    diff -= 360
                elif diff < -180:
                    diff += 360

                # Calculate incremental step for this motor
                position_step = diff / steps
                new_positions[motor_id] = current_position + position_step * (step + 1)

            # Set new goal positions for all motors
            dxl_io.set_goal_position(new_positions)

            # Wait for the step duration
            t.sleep(step_duration)

        print(f"All motors moved to their target positions over {duration} seconds.")

    finally:
        dxl_io.close()



        # # Update the motor's position for this step BROKEN - DO we need a manual step at -180 / 180?
        # if current_position < 0:
        #     if (current_position - position_step * (step +1)) <= -180:
        #         new_positions[motor_id] = current_position - position_step * (step + 1)
        #     else:
        #         new_positions[motor_id] = 180 - position_step * (step + 1)
        # elif current_position > 0:
        #     if(current_position + position_step * (step + 1)) >= 180:
        #         new_positions[motor_id] = current_position + position_step * (step + 1)
        #     else:
        #         new_positions[motor_id] = - 180 + position_step * (step + 1)


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
            # print(formatted_positions)
            
            return positions
        else:
            print("Some motors are not reachable.")
            return positions
    finally:
        dxl_io.close()

def get_motor_position(motor_id):
    dxl_io = pypot.dynamixel.DxlIO(PORT, BAUDRATE)
    
    try:
        # Check if the motor is reachable
        if dxl_io.ping(motor_id):
            # Get the current position of the specified motor
            position = dxl_io.get_present_position([motor_id])[0]  # get_present_position returns a list
            motor_name = motor_names.get(motor_id, 'Unknown Motor')
            
            # Print the motor name and position
            print(f"{motor_name} (ID: {motor_id}) is at position {position}.")
            
            return position
        else:
            print(f"Motor {motor_id} is not reachable.")
            return None
    finally:
        dxl_io.close()


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


# Poppy Actions

def start_position(duration=2):
    # Initialize the positions
    target_positions = {
        R_SHOULDER_Y: 150.73,
        R_SHOULDER_X: -107.82,
        R_ARM_Z: -20.7,
        R_ELBOW_Y: 171.38,
        L_SHOULDER_Y: -1,
        L_SHOULDER_X: 23.78,
        L_ARM_Z: 13.41,
        L_ELBOW_Y: -179.0,
        HEAD_Y: -3.96,
        HEAD_Z: -77.27,
        BUST_X: -1,
        BUST_Y: -8.22,
        ABS_Z: -4.53
    }
    
    move_motors_timed(target_positions, duration)

def wave_poppy(duration=2):
    reset_stop_flag()

    def maybe_stop():
        if stop_flag:
            print("Wave interrupted!")
            return True
        return False

    # Step 1 - Initial wave position
    target_positions = {
        R_SHOULDER_Y: 123.96,
        R_SHOULDER_X: -94.02,
        R_ARM_Z: -29.85,
        R_ELBOW_Y: -154.15,
        L_SHOULDER_Y: -40.92,
        L_SHOULDER_X: -11.91,
        L_ARM_Z: -2.86,
        L_ELBOW_Y: -145.45,
        HEAD_Y: -14.25,
        HEAD_Z: -106.6,
    }
    if maybe_stop(): return
    move_motors_timed(target_positions, duration)
    if maybe_stop(): return
    t.sleep(0.5)

    # Step 2 - Raise left arm for waving
    target_positions_2 = {
        R_SHOULDER_Y: 103.67,
        R_SHOULDER_X: -94.99,
        R_ARM_Z: -25.01,
        R_ELBOW_Y: -156.44,
        L_SHOULDER_Y: -77.85,
        L_SHOULDER_X: 26.77,
        L_ARM_Z: 34.07,
        L_ELBOW_Y: -144.66,
        HEAD_Y: -4.25,
        HEAD_Z: -86.6,
    }
    if maybe_stop(): return
    move_motors_timed(target_positions_2, duration)
    if maybe_stop(): return
    t.sleep(1)

    # Step 3 - Return to neutral wave position
    target_positions_3 = {
        R_SHOULDER_Y: 123.96,
        R_SHOULDER_X: -94.02,
        R_ARM_Z: -29.85,
        R_ELBOW_Y: -154.15,
        L_SHOULDER_Y: -45.92,
        L_SHOULDER_X: -15.91,
        L_ARM_Z: -2.86,
        L_ELBOW_Y: -145.45,
        HEAD_Y: -24.25,
        HEAD_Z: -116.6,
    }
    if maybe_stop(): return
    move_motors_timed(target_positions_3, duration)
    if maybe_stop(): return
    t.sleep(0.5)

    # Step 4 - Second wave gesture
    target_positions_4 = {
        R_SHOULDER_Y: 103.67,
        R_SHOULDER_X: -94.99,
        R_ARM_Z: -25.01,
        R_ELBOW_Y: -156.44,
        L_SHOULDER_Y: -67.85,
        L_SHOULDER_X: 29.77,
        L_ARM_Z: 34.07,
        L_ELBOW_Y: -144.66,
        HEAD_Y: -4.25,
        HEAD_Z: -96.6,
    }
    if maybe_stop(): return
    move_motors_timed(target_positions_4, duration)
    if maybe_stop(): return
    t.sleep(0.5)

def wave_more_poppy():
    reset_stop_flag()

    def maybe_stop():
        if stop_flag:
            print("Wave loop interrupted!")
            return True
        return False

    while True:
        if maybe_stop(): break
        wave_poppy(2)
        if maybe_stop(): break
        t.sleep(15)


def ymca(duration=1):
    # Y
    target_positions = {
        R_SHOULDER_Y: -109.05,
        R_SHOULDER_X: -62.9,
        R_ARM_Z: -60.26,
        R_ELBOW_Y: 133.49,
        L_SHOULDER_Y: -109.58,
        L_SHOULDER_X: -4.88,
        L_ARM_Z: 60.7,
        L_ELBOW_Y: -98.33,
        HEAD_Y: -3.96,
        HEAD_Z: -77.27,
        # BUST_X: -1,
        # BUST_Y: -8.22,
        # ABS_Z: -4.53
    }

    move_motors_timed(target_positions, duration)

    t.sleep(0.5)

    # # M
    # target_positions_2 = {
    #     R_SHOULDER_Y: -96.57,
    #     R_SHOULDER_X: -79.43,
    #     R_ARM_Z: -68.09,
    #     R_ELBOW_Y: -142.37,
    #     L_SHOULDER_Y: -131.03,
    #     L_SHOULDER_X: 14.55,
    #     L_ARM_Z: 75.91,
    #     L_ELBOW_Y: -177.1,
    #     HEAD_Y: -3.96,
    #     HEAD_Z: -77.27,
    #     BUST_X: -1,
    #     BUST_Y: -8.22,
    #     ABS_Z: -4.53
    # }

    # move_motors_timed(target_positions_2, duration)

    # t.sleep(0.5)

    # # C
    # target_positions_3 = {
    #     R_SHOULDER_Y: -96.57,
    #     R_SHOULDER_X: -79.43,
    #     R_ARM_Z: -68.09,
    #     R_ELBOW_Y: -142.37,
    #     L_SHOULDER_Y: 54.81,
    #     L_SHOULDER_X: 6.29,
    #     L_ARM_Z: -102.02,
    #     L_ELBOW_Y: -153.27,
    #     HEAD_Y: -3.96,
    #     HEAD_Z: -77.27,
    #     BUST_X: -1,
    #     BUST_Y: -8.22,
    #     ABS_Z: -4.53
    # }

    # move_motors_timed(target_positions_3, duration)

    # t.sleep(0.1)

    # # A
    # target_positions_4 = {
    #     R_SHOULDER_Y: -86.11,
    #     R_SHOULDER_X: -116.18,
    #     R_ARM_Z: -65.98,
    #     R_ELBOW_Y: 145.01,
    #     L_SHOULDER_Y: -120.13,
    #     L_SHOULDER_X: 43.03,
    #     L_ARM_Z: 82.95,
    #     L_ELBOW_Y: -98.86,
    #     HEAD_Y: -3.96,
    #     HEAD_Z: -77.27,
    #     BUST_X: -1,
    #     BUST_Y: -8.22,
    #     ABS_Z: -4.53
    # }

    # move_motors_timed(target_positions_4, duration)

    # t.sleep(0.5)


def macarena(duration=0.5):
    reset_stop_flag()

    def maybe_stop():
        if stop_flag:
            print("Macarena interrupted!")
            return True
        return False

    steps = [
        # Step 1 - R arm out
        {
            R_SHOULDER_Y: 175.52, R_SHOULDER_X: -99.3, R_ARM_Z: -86.46, R_ELBOW_Y: 135.34,
            L_SHOULDER_Y: 51.3, L_SHOULDER_X: 31.87, L_ARM_Z: -9.1, L_ELBOW_Y: -150.9
        },
        # Step 2 - L arm out
        {
            R_SHOULDER_Y: 175.52, R_SHOULDER_X: -99.3, R_ARM_Z: -86.46, R_ELBOW_Y: 135.34,
            L_SHOULDER_Y: -9.89, L_SHOULDER_X: 31.25, L_ARM_Z: 58.15, L_ELBOW_Y: -99.65
        },
        # Step 3 - Turn R arm
        {
            R_SHOULDER_Y: 175.52, R_SHOULDER_X: -108.09, R_ARM_Z: 83.46, R_ELBOW_Y: 135.34,
            L_SHOULDER_Y: -9.89, L_SHOULDER_X: 31.25, L_ARM_Z: 58.15, L_ELBOW_Y: -99.65
        },
         # Step 4 - Turn L arm
        {
            L_SHOULDER_Y: -21.89, L_SHOULDER_X: 34.25, L_ARM_Z: -115.21, L_ELBOW_Y: -99.65,
            R_SHOULDER_Y: 175.52, R_SHOULDER_X: -108.09, R_ARM_Z: 83.46, R_ELBOW_Y: 135.34
        },
       # Step 5 - R arm to shoulder
        {
            L_SHOULDER_Y: -21.89, L_SHOULDER_X: 34.25, L_ARM_Z: -115.21, L_ELBOW_Y: -99.65,
            R_SHOULDER_Y: 180, R_SHOULDER_X: -103.65, R_ARM_Z: -80.76, R_ELBOW_Y: 179
        },
        # Step 6a - L arm to shoulder
        {
            L_SHOULDER_Y: -5, L_SHOULDER_X: -7, L_ARM_Z: 0, L_ELBOW_Y: -75,
            R_SHOULDER_Y: 180, R_SHOULDER_X: -103.65, R_ARM_Z: -80.76, R_ELBOW_Y: 179
        },
        # Step 6b
        {
            L_SHOULDER_Y: 5.58, L_SHOULDER_X: 23.25, L_ARM_Z: 69.5, L_ELBOW_Y: -175,
            R_SHOULDER_Y: 180, R_SHOULDER_X: -103.65, R_ARM_Z: -80.76, R_ELBOW_Y: 179
        },
        # Step 7- R arm to head
        {
            L_SHOULDER_Y: 5.58, L_SHOULDER_X: 23.25, L_ARM_Z: 69.5, L_ELBOW_Y: -175,
            R_SHOULDER_Y: -120, R_SHOULDER_X: -100, R_ARM_Z: -50, R_ELBOW_Y: 179
        },
        # Step 7b
        {
            L_SHOULDER_Y: 5.58, L_SHOULDER_X: 23.25, L_ARM_Z: 69.5, L_ELBOW_Y: -175,
            R_SHOULDER_Y: 110, R_SHOULDER_X: 56, R_ARM_Z: 80, R_ELBOW_Y: 179
        },
        # Step 8- L arm to head
        {
            L_SHOULDER_Y: -120, L_SHOULDER_X: 27, L_ARM_Z: 73, L_ELBOW_Y: -130,
            R_SHOULDER_Y: 110, R_SHOULDER_X: 56, R_ARM_Z: 80, R_ELBOW_Y: 179
        },
        # Step 9a - R arm to L hip
        {
            L_SHOULDER_Y: -120, L_SHOULDER_X: 27, L_ARM_Z: 73, L_ELBOW_Y: -125,
            R_SHOULDER_Y: 177, R_SHOULDER_X: -103, R_ARM_Z: -80, R_ELBOW_Y: 130
        },
        # Step 9b
        {
            L_SHOULDER_Y: -120, L_SHOULDER_X: 27, L_ARM_Z: 73, L_ELBOW_Y: -125,
            R_SHOULDER_Y: 123, R_SHOULDER_X: -122, R_ARM_Z: -98, R_ELBOW_Y: 179
        },
        # Step 10a- L arm to R hip
        {
            L_SHOULDER_Y: -20, L_SHOULDER_X: 15, L_ARM_Z: 61, L_ELBOW_Y: -121,
            R_SHOULDER_Y: 123, R_SHOULDER_X: -122, R_ARM_Z: -98, R_ELBOW_Y: 179
        },
        # Step 10b
        {
            L_SHOULDER_Y: 20, L_SHOULDER_X: 50, L_ARM_Z: 79, L_ELBOW_Y: -132,
            R_SHOULDER_Y: 123, R_SHOULDER_X: -122, R_ARM_Z: -98, R_ELBOW_Y: 179
        },
        # Step 11a- R arm to R hip
        {
            L_SHOULDER_Y: 15, L_SHOULDER_X: 35, L_ARM_Z: 60, L_ELBOW_Y: -132,
            R_SHOULDER_Y: 135, R_SHOULDER_X: -85, R_ARM_Z: -78, R_ELBOW_Y: 179
        },
        # Step 11b (same as 11a)
        {
            L_SHOULDER_Y: 15, L_SHOULDER_X: 35, L_ARM_Z: 60, L_ELBOW_Y: -132,
            R_SHOULDER_Y: 135, R_SHOULDER_X: -85, R_ARM_Z: -78, R_ELBOW_Y: 179
        },
        # Step 12- L arm to L hip
        {
            L_SHOULDER_Y: 33, L_SHOULDER_X: 5, L_ARM_Z: 45, L_ELBOW_Y: -143,
            R_SHOULDER_Y: 135, R_SHOULDER_X: -85, R_ARM_Z: -78, R_ELBOW_Y: 179
        },
        # Step 13a- Clap
        {
            L_SHOULDER_Y: 25, L_SHOULDER_X: 9, L_ARM_Z: -42, L_ELBOW_Y: -104,
            R_SHOULDER_Y: 132, R_SHOULDER_X: -80, R_ARM_Z: 23, R_ELBOW_Y: 165
        },
        # Step 13b- Clap
        {
            L_SHOULDER_Y: 1, L_SHOULDER_X: 44, L_ARM_Z: 12, L_ELBOW_Y: -123,
            R_SHOULDER_Y: 152, R_SHOULDER_X: -116, R_ARM_Z: -13, R_ELBOW_Y: 175
        }
    ]

    for i, pose in enumerate(steps):
        if maybe_stop():
            return
        move_motors_timed(pose, (duration/3 if "6" in str(i) or "7" in str(i) or "9" in str(i) or "10" in str(i) or "11" in str(i) or "13" in str(i) else duration))
        if maybe_stop():
            return
        t.sleep(0.1 if "b" in str(i) else 0.5)

def macarena_5():
    def maybe_stop():
        if stop_flag:
            print("macarena_5 loop interrupted!")
            return True
        return False

    if maybe_stop(): return
    macarena()
    if maybe_stop(): return
    t.sleep(1)
    
    macarena()
    if maybe_stop(): return
    t.sleep(1)

    macarena()
    if maybe_stop(): return
    t.sleep(1)

    macarena()
    if maybe_stop(): return
    t.sleep(1)

    macarena()
    if maybe_stop(): return
    t.sleep(1)

    macarena()
    if maybe_stop(): return
    t.sleep(1)

    macarena()
    if maybe_stop(): return
    t.sleep(1)

    macarena()
    if maybe_stop(): return
    t.sleep(1)

    macarena()


