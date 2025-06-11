import tkinter as tk
import time as t
import poppy_motors as pm


# tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Poppy Motor Control")
    # Set a fixed window size (e.g., 300x400 pixels)
    root.geometry("600x800")  # Width x Height

    # Dictionary to hold current position and goal entry variables for each motor
    entry_vars = {}
    goal_vars = {}

    # Function to display and update motor positions
    def display_motor_positions():
        positions = pm.get_all_motor_positions()  # Fetch motor positions
        for motor_name, position in positions.items():
            if motor_name in entry_vars:
                entry_vars[motor_name][0].set(f"{position:.2f}")  # Update the StringVar associated with the Entry
        root.after(500, display_motor_positions)  # Update every 500ms


    # Start Position Button
    start_button = tk.Button(root, text="Start Position", command=pm.start_position)
    start_button.pack(pady=10)

    # Wave Button
    wave_button = tk.Button(root, text="Wave Poppy", command=pm.wave_poppy)
    wave_button.pack(pady=10)

    # Wave Button
    wave_button = tk.Button(root, text="Wave repeated", command=pm.wave_more_poppy)
    wave_button.pack(pady=10)

    # Wave Button
    wave_button = tk.Button(root, text="YMCA", command=pm.ymca)
    wave_button.pack(pady=10)

    # Macarena Button
    macarena_button = tk.Button(root, text="Macarena", command=pm.macarena)
    macarena_button.pack(pady=10)

    # Relax Motors Button
    relax_arms_button = tk.Button(root, text="Relax Arms Only", command=pm.relax_arms)
    relax_arms_button.pack(pady=10)

    # Relax Motors Button
    relax_button = tk.Button(root, text="Relax All Motors", command=pm.relax_all_motors)
    relax_button.pack(pady=10)

    # Get Motor Positions
    motor_positions_button = tk.Button(root, text="Display Motor Positions", command=pm.get_all_motor_positions)
    motor_positions_button.pack(pady=10)

    # Create a frame to hold motor position labels and entry fields
    motor_frame = tk.Frame(root)
    motor_frame.pack(pady=20)

    # Create labels, current angle entry, desired angle entry, and go buttons for each motor
    for motor_id, motor_name in pm.motor_names.items():
        # Display the motor name
        label = tk.Label(motor_frame, text=f"{motor_name}:")
        label.grid(row=motor_id, column=0)
        
        # Entry for current angle (this will display the actual current angle)
        current_angle_var = tk.StringVar()
        current_angle_entry = tk.Entry(motor_frame, textvariable=current_angle_var)
        current_angle_entry.grid(row=motor_id, column=1)

        # Placeholder for desired angle input
        desired_angle_var = tk.StringVar()
        desired_angle_entry = tk.Entry(motor_frame, textvariable=desired_angle_var)
        desired_angle_entry.grid(row=motor_id, column=2)
        
        # "Go" button to call move_motor_instant
        go_button = tk.Button(motor_frame, text="Go", 
                              command=lambda m_id=motor_id, var=desired_angle_var: pm.move_motor_instant(m_id, var.get()))
        go_button.grid(row=motor_id, column=3)
        
        # Save the entry variables for later use if needed
        entry_vars[motor_name] = (current_angle_var, desired_angle_var)

    # Automatically fetch and display motor positions when the GUI starts
    display_motor_positions()


# Launch the GUI
if __name__ == "__main__":
    create_gui()