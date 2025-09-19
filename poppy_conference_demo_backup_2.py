import tkinter as tk
import time as t
import poppy_motors as pm
import threading



# tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Poppy Motor Control")
    # Set a fixed window size (e.g., 300x400 pixels)
    root.geometry("600x800")  # Width x Height

    def threaded_command(command):
        threading.Thread(target=command).start()


    # Dictionary to hold current position and goal entry variables for each motor
    entry_vars = {}
    goal_vars = {}

    # Function to display and update motor positions
    def display_motor_positions():
        positions = pm.get_all_motor_positions()  # Fetch motor positions
        for motor_name, position in positions.items():
            if motor_name in entry_vars:
                entry_vars[motor_name].set(f"{position:.2f}")  # Update the StringVar associated with the Entry
        root.after(500, display_motor_positions)  # Update every 500ms


    # Start Position Button
    start_button = tk.Button(root, text="Start Position", command=pm.start_position)
    start_button.pack(pady=10)

    # Wave Button  (with threading)
    wave_button = tk.Button(root, text="Wave Poppy", command=lambda: threaded_command(pm.wave_poppy))
    wave_button.pack(pady=10)

    # Wave Button  (with threading)
    wave_button = tk.Button(root, text="Wave repeated", command=lambda: threaded_command(pm.wave_more_poppy))
    wave_button.pack(pady=10)

    # Wave Button  (with threading)
    wave_button = tk.Button(root, text="YMCA", command=lambda: threaded_command(pm.ymca))
    wave_button.pack(pady=10)

    # Macarena Button  (with threading)
    macarena_button = tk.Button(root, text="Macarena", command=lambda: threaded_command(pm.macarena))
    macarena_button.pack(pady=10)

    # Macarena Button x5 (with threading)
    macarena_button = tk.Button(root, text="Macarena x5", command=lambda: threaded_command(pm.macarena_5))
    macarena_button.pack(pady=10)

    # STOP Button
    stop_button = tk.Button(root, text="STOP", bg="red", fg="white",  font=("Arial", 14, "bold"),
                        command=pm.stop_motion)
    stop_button.pack(pady=10)

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

    # Create labels, current angle, desired angle entries, and go buttons for each motor
    for motor_id, motor_name in pm.motor_names.items():
        # Display the motor name
        label = tk.Label(motor_frame, text=f"{motor_name}:")
        label.grid(row=motor_id, column=0)
        
        # Display the current angle (you may need to update this with actual motor positions)
        current_angle_label = tk.Label(motor_frame, text="0")  # Placeholder for current angle
        current_angle_label.grid(row=motor_id, column=1)
        
        # Entry for desired angle
        desired_angle_var = tk.StringVar()
        desired_angle_entry = tk.Entry(motor_frame, textvariable=desired_angle_var)
        desired_angle_entry.grid(row=motor_id, column=2)
        
        # "Go" button to call move_motor_instant
        go_button = tk.Button(motor_frame, text="Go", 
                            command=lambda m_id=motor_id, var=desired_angle_var: pm.move_motor_instant(m_id, var.get()))
        go_button.grid(row=motor_id, column=3)
        
        # Save the entry variables for later use if needed
        entry_vars[motor_name] = desired_angle_var

    # Automatically fetch and display motor positions when the GUI starts
    display_motor_positions()

    root.mainloop()

# Launch the GUI
if __name__ == "__main__":
    create_gui()