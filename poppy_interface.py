import tkinter as tk
import poppy_motors as pm


# tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Poppy Motor Control")
    root.geometry("600x800")  # Set a fixed window size (e.g., 600x800 pixels)

    # Dictionary to hold current position and goal entry variables for each motor
    entry_vars = {}
    goal_vars = {}

    # Function to display and update motor positions
    def display_motor_positions():
        positions = pm.get_all_motor_positions()  # Fetch motor positions
        for motor_name, position in positions.items():
            if motor_name in entry_vars:
                entry_vars[motor_name].set(f"{position:.2f}")  # Update the read-only field with the current position
        root.after(500, display_motor_positions)  # Update every 500ms

    # Function to move motor when goal position is entered
    def move_motor(motor_id, motor_name):
        try:
            goal_position = float(goal_vars[motor_name].get())  # Get the goal position from the entry
            pm.move_motor_instant(motor_id, goal_position)  # Move motor to the goal position
        except ValueError:
            print(f"Invalid position entered for {motor_name}")

    # Start Position Button
    start_button = tk.Button(root, text="Start Position", command=pm.start_position)
    start_button.pack(pady=10)

    # Wave Button
    wave_button = tk.Button(root, text="Wave Poppy", command=pm.wave_poppy)
    wave_button.pack(pady=10)

    # Wave More Button
    wave_more_button = tk.Button(root, text="Wave repeated", command=pm.wave_more_poppy)
    wave_more_button.pack(pady=10)

    # YMCA Button
    ymca_button = tk.Button(root, text="YMCA", command=pm.ymca)
    ymca_button.pack(pady=10)

    # Relax Arms Button
    relax_arms_button = tk.Button(root, text="Relax Arms Only", command=pm.relax_arms)
    relax_arms_button.pack(pady=10)

    # Relax All Motors Button
    relax_button = tk.Button(root, text="Relax All Motors", command=pm.relax_all_motors)
    relax_button.pack(pady=10)

    # Create a frame to hold motor position labels and entry fields
    motor_frame = tk.Frame(root)
    motor_frame.pack(pady=20)

    # Create labels, current position (read-only) fields, and goal position (editable) fields for each motor
    for motor_id, motor_name in pm.motor_names.items():
        # Label for motor name
        label = tk.Label(motor_frame, text=f"{motor_name}:")
        label.grid(row=motor_id, column=0)

        # Read-only entry to display current motor position
        entry_var = tk.StringVar()
        current_position = tk.Entry(motor_frame, textvariable=entry_var, state='readonly')  # Read-only
        current_position.grid(row=motor_id, column=1)
        entry_vars[motor_name] = entry_var  # Save the StringVar for updating motor position

        # Editable entry for goal position input
        goal_var = tk.StringVar()
        goal_position_entry = tk.Entry(motor_frame, textvariable=goal_var)  # Editable
        goal_position_entry.grid(row=motor_id, column=2)
        goal_vars[motor_name] = goal_var  # Save the StringVar for retrieving goal position

        # Bind the 'Return' (Enter) key to move the motor when goal position is entered
        goal_position_entry.bind("<Return>", lambda event, mid=motor_id, mname=motor_name: move_motor(mid, mname))

    # Automatically fetch and display motor positions when the GUI starts
    display_motor_positions()

    root.mainloop()


# Launch the GUI
if __name__ == "__main__":
    create_gui()
