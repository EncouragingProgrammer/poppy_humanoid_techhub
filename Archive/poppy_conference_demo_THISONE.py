import tkinter as tk
import poppy_motors as pm

# tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Poppy Motor Control")
    root.geometry("600x800")  # Width x Height

    # Dictionary to hold current position and goal entry variables for each motor
    entry_vars = {}

    # Function to display and update motor positions
    def display_motor_positions():
        try:
            positions = pm.get_all_motor_positions()  # Fetch motor positions
            for motor_name, position in positions.items():
                if motor_name in entry_vars:
                    entry_vars[motor_name]["current"].config(text=f"{position:.2f}")
        except Exception as e:
            print(f"Error fetching motor positions: {e}")
        root.after(10, display_motor_positions)  # Update every 100ms

    # Control buttons
    tk.Button(root, text="Start Position", command=pm.start_position).pack(pady=10)
    tk.Button(root, text="Wave Poppy", command=pm.wave_poppy).pack(pady=10)
    tk.Button(root, text="Wave repeated", command=pm.wave_more_poppy).pack(pady=10)
    tk.Button(root, text="YMCA", command=pm.ymca).pack(pady=10)
    tk.Button(root, text="Macarena", command=pm.macarena).pack(pady=10)
    tk.Button(root, text="Macarena x5", command=pm.macarena_5).pack(pady=10)
    tk.Button(root, text="Relax Arms Only", command=pm.relax_arms).pack(pady=10)
    tk.Button(root, text="Relax All Motors", command=pm.relax_all_motors).pack(pady=10)
    tk.Button(root, text="Display Motor Positions", command=pm.get_all_motor_positions).pack(pady=10)

    # Create a frame to hold motor position labels and entry fields
    motor_frame = tk.Frame(root)
    motor_frame.pack(pady=20)

    # Create labels, current angle, desired angle entries, and go buttons for each motor
    for motor_id, motor_name in pm.motor_names.items():
        # Motor name label
        label = tk.Label(motor_frame, text=f"{motor_name}:")
        label.grid(row=motor_id, column=0)
        
        # Display current angle with a label that can be updated
        current_angle_label = tk.Label(motor_frame, text="0")
        current_angle_label.grid(row=motor_id, column=1)

        # Entry for desired angle, ensuring it's enabled and ready for typing
        desired_angle_var = tk.StringVar()
        desired_angle_entry = tk.Entry(motor_frame, textvariable=desired_angle_var, state="normal")
        desired_angle_entry.grid(row=motor_id, column=2)
        
        # "Go" button to call move_motor_instant
        go_button = tk.Button(motor_frame, text="Go", 
                              command=lambda m_id=motor_id, var=desired_angle_var: pm.move_motor_instant(m_id, var.get()))
        go_button.grid(row=motor_id, column=3)
        
        # Store the current angle label and desired angle variable in entry_vars
        entry_vars[motor_name] = {"current": current_angle_label, "desired": desired_angle_var}

    # Automatically fetch and display motor positions when the GUI starts
    display_motor_positions()

    root.mainloop()

# Launch the GUI
if __name__ == "__main__":
    create_gui()
