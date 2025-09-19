# poppy_touch_ui.py
import tkinter as tk
import poppy_motors as pm

def create_touch_gui():
    root = tk.Tk()
    root.title("Poppy Control")
    root.geometry("480x320")  # Fits most 4-inch Pi screens

    # Style helper for big buttons
    def big_button(text, command, color="lightgray"):
        return tk.Button(
            root, text=text, command=command,
            width=15, height=3,
            bg=color, font=("Arial", 16, "bold")
        )

    # Buttons
    big_button("Wave 👋", pm.wave_poppy, "#90ee90").pack(pady=10)
    big_button("Drive 🚗", pm.drive_pose, "#add8e6").pack(pady=10)
    big_button("Hands Up 🙌", pm.hands_up, "#ffd580").pack(pady=10)
    big_button("Rest 😴", pm.rest_pose, "#d3d3d3").pack(pady=10)

    # STOP button (red & centered at bottom)
    tk.Button(
        root, text="STOP", command=pm.stop_motion,
        bg="red", fg="white", font=("Arial", 20, "bold"),
        width=20, height=3
    ).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_touch_gui()
