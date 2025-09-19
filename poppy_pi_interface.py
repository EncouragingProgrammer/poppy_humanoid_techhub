# poppy_touch_ui.py
import tkinter as tk
import poppy_motors as pm

def create_touch_gui():
    root = tk.Tk()
    root.title("Poppy Control")
    root.geometry("480x320")  # Fits most 4-inch Pi screens
    root.configure(bg="black")

    def big_button(text, command, color="lightgray", row=0, col=0):
        btn = tk.Button(
            root, text=text, command=command,
            width=12, height=4,
            bg=color, font=("Arial", 14, "bold")
        )
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    # Arrange in 2x2 grid + STOP spanning bottom row
    big_button("Wave 👋", pm.wave_poppy, "#90ee90", row=0, col=0)
    big_button("Drive 🚗", pm.drive_pose, "#add8e6", row=0, col=1)
    big_button("Hands Up 🙌", pm.hands_up, "#ffd580", row=1, col=0)
    big_button("Rest 😴", pm.rest_pose, "#d3d3d3", row=1, col=1)

    stop_btn = tk.Button(
        root, text="STOP", command=pm.stop_motion,
        bg="red", fg="white", font=("Arial", 20, "bold"),
        width=25, height=2
    )
    stop_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

    # Make grid resize nicely
    root.grid_rowconfigure([0, 1, 2], weight=1)
    root.grid_columnconfigure([0, 1], weight=1)

    root.mainloop()

if __name__ == "__main__":
    create_touch_gui()
