# poppy_motor_test_ui.py
import tkinter as tk
import poppy_motors as pm

def create_motor_test_gui():
    root = tk.Tk()
    root.title("Poppy Motor Test")
    root.geometry("480x320")  # For Pi touchscreen

    entry_vars = {}

    # Scrollable frame setup
    canvas = tk.Canvas(root, width=460, height=300)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Headers
    headers = ["Motor", "Current", "Set Position", "Set", "Hold", "Release"]
    for col, text in enumerate(headers):
        tk.Label(scroll_frame, text=text, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=3, pady=3)
    
    # Update positions live
    def update_positions():
        try:
            positions = pm.get_all_motor_positions()
            for motor_name, pos in positions.items():
                if motor_name in entry_vars:
                    entry_vars[motor_name]["current"].config(text=f"{pos:.1f}")
        except Exception as e:
            print(f"Error fetching motor positions: {e}")
        root.after(300, update_positions)

    # Create rows
    for row, (motor_id, motor_name) in enumerate(pm.motor_names.items(), start=1):
        # Motor name
        tk.Label(scroll_frame, text=motor_name).grid(row=row, column=0, padx=3, pady=3)

        # Current position
        current_label = tk.Label(scroll_frame, text="0")
        current_label.grid(row=row, column=1, padx=3, pady=3)

        # Desired entry
        desired_var = tk.StringVar()
        tk.Entry(scroll_frame, textvariable=desired_var, width=6).grid(row=row, column=2, padx=3, pady=3)

        # Set button → use desired entry value
        tk.Button(
            scroll_frame, text="Set", width=5,
            command=lambda m=motor_id, v=desired_var: pm.move_motor_instant(m, v.get())
        ).grid(row=row, column=3, padx=3, pady=3)

        # Hold button → use current label value
        tk.Button(
            scroll_frame, text="Hold", width=5,
            command=lambda m=motor_id, l=current_label: pm.move_motor_instant(m, l.cget("text"))
        ).grid(row=row, column=4, padx=3, pady=3)

        # Release button
        tk.Button(
            scroll_frame, text="Release", width=6,
            command=lambda m=motor_id: pm.relax_motors([m])
        ).grid(row=row, column=5, padx=3, pady=3)

        # Store for updates
        entry_vars[motor_name] = {"current": current_label, "desired": desired_var}

    # When the window closes, release motor connection
    def on_close():
        pm.close_connection()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Kick off updates
    update_positions()
    root.mainloop()

if __name__ == "__main__":
    create_motor_test_gui()
