import tkinter as tk
import time
import pypot
from pypot.creatures import PoppyTorso


class PoppyRobotController:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Poppy Robot Controller")
        self.is_running = False
        self.poppy = None

        # Create buttons to control the robot
        self.create_buttons()
        self.update_status_label()

        self.window.mainloop()

    def create_buttons(self):
        # Create frame for start and stop buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(side="left", padx=10, pady=10)
        start_button = tk.Button(
            button_frame, text="Start Robot", command=self.start_robot)
        start_button.pack(side="top", padx=10, pady=10)
        stop_button = tk.Button(
            button_frame, text="Stop Robot", command=lambda: self.stop_robot(self.poppy))
        stop_button.pack(side="top", padx=10, pady=10)

        # Create frame for robot status and controls
        control_frame = tk.Frame(self.window)
        control_frame.pack(side="right", padx=10, pady=10)
        self.robot_status = tk.Label(self.window, text="Poppy Stopped", fg="red")
        self.robot_status.pack(in_=control_frame, side="top", padx=10, pady=10)
        start_position_button = tk.Button(
            control_frame, text="Start Position", command=lambda: self.start_position(self.poppy))
        start_position_button.pack(side="left")
        wave_button = tk.Button(
            control_frame, text="Wave Hand", command=lambda: self.wave_hand(self.poppy))
        wave_button.pack(side="left")
        dance_button = tk.Button(
            control_frame, text="Dance", command=lambda: self.dance_ymca(self.poppy))
        dance_button.pack(side="left")
        y_button = tk.Button(control_frame, text="Y",
                             command=lambda: self.move_y(self.poppy, 1))
        y_button.pack(side="left")
        m_button = tk.Button(control_frame, text="M",
                             command=lambda: self.move_m(self.poppy, 1))
        m_button.pack(side="left")
        c_button = tk.Button(control_frame, text="C",
                             command=lambda: self.move_c(self.poppy, 1))
        c_button.pack(side="left")
        a_button = tk.Button(control_frame, text="A",
                             command=lambda: self.move_a(self.poppy, 1))
        a_button.pack(side="left")


    def wave_hand(self, poppy):
        # Code to make the robot wave its hand
        print("Waving hand...")
        # Move arm back to starting position
        self.start_position(poppy)

        # Raise arm to wave
        poppy.l_shoulder_x.goto_position(75, 1, wait=False)
        poppy.l_arm_z.goto_position(85, 1, wait=False)

        # Wave hand
        for i in range(2):
            poppy.l_elbow_y.goto_position(-50, 1, wait=True)
            poppy.l_elbow_y.goto_position(-110, 1, wait=True)
            time.sleep(0.1)
            poppy.head_z.goto_position(20, 1, wait=False)
            poppy.l_elbow_y.goto_position(-55, 1, wait=True)
            poppy.l_elbow_y.goto_position(-105, 1, wait=True)
            time.sleep(0.1)
            poppy.head_z.goto_position(0, 1, wait=False)

        # Move arm back to starting position
        self.start_position(poppy)

    def dance_ymca(self, poppy):
        print("Dancing YMCA!")
        self.start_position(poppy)
        time.sleep(1)
        self.move_y(poppy, 1)
        time.sleep(0.5)
        self.move_m(poppy, 1)
        time.sleep(0.5)
        self.move_c(poppy, 0.5)
        time.sleep(0.5)
        self.move_a(poppy, 1)
        time.sleep(0.5)
        print("Finished dancing YMCA!")
        time.sleep(2)
        self.start_position(poppy)

    def move_y(self, poppy, speed):
        # Move robot to Y position
        poppy.l_shoulder_x.goto_position(140, speed, wait=False)
        poppy.l_shoulder_y.goto_position(0, speed, wait=False)
        poppy.l_arm_z.goto_position(85, speed, wait=False)
        poppy.l_elbow_y.goto_position(-20, speed, wait=False)
        poppy.r_shoulder_x.goto_position(-140, speed, wait=False)
        poppy.r_shoulder_y.goto_position(0, speed, wait=False)
        poppy.r_arm_z.goto_position(-85, speed, wait=False)
        poppy.r_elbow_y.goto_position(-20, speed, wait=False)
        poppy.head_z.goto_position(0, speed, wait=False)

    def move_m(self, poppy, speed):
        # Move robot to M position
        poppy.l_shoulder_x.goto_position(150, speed, wait=False)
        poppy.l_shoulder_y.goto_position(0, speed, wait=False)
        poppy.l_arm_z.goto_position(90, speed, wait=False)
        poppy.l_elbow_y.goto_position(-100, speed, wait=False)
        poppy.r_shoulder_x.goto_position(-150, speed, wait=False)
        poppy.r_shoulder_y.goto_position(0, speed, wait=False)
        poppy.r_arm_z.goto_position(-90, speed, wait=False)
        poppy.r_elbow_y.goto_position(-100, speed, wait=False)
        poppy.head_z.goto_position(0, speed, wait=False)

    def move_c(self, poppy, speed):
        # Move robot to C position
        poppy.l_shoulder_x.goto_position(0, speed, wait=False)
        poppy.l_shoulder_y.goto_position(0, speed, wait=False)
        poppy.l_arm_z.goto_position(90, speed, wait=False)
        poppy.l_elbow_y.goto_position(-80, speed, wait=False)
        poppy.r_shoulder_x.goto_position(-170, speed, wait=False)
        poppy.r_shoulder_y.goto_position(0, speed, wait=False)
        poppy.r_arm_z.goto_position(-90, speed, wait=False)
        poppy.r_elbow_y.goto_position(-80, speed, wait=False)
        poppy.head_z.goto_position(0, speed, wait=False)

    def move_a(self, poppy, speed):
        # Move robot to A position
        poppy.l_shoulder_x.goto_position(180, speed, wait=False)
        poppy.l_shoulder_y.goto_position(0, speed, wait=False)
        poppy.l_arm_z.goto_position(90, speed, wait=False)
        poppy.l_elbow_y.goto_position(-20, speed, wait=False)
        poppy.r_shoulder_x.goto_position(-180, speed, wait=False)
        poppy.r_shoulder_y.goto_position(0, speed, wait=False)
        poppy.r_arm_z.goto_position(-90, speed, wait=False)
        poppy.r_elbow_y.goto_position(-20, speed, wait=False)
        poppy.head_z.goto_position(0, speed, wait=False)

    def start_position(self, poppy):
        # Move robot to start position
        print("Moving to start position...")
        poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        poppy.l_shoulder_y.goto_position(0, 1, wait=False)
        poppy.l_arm_z.goto_position(0, 1, wait=False)
        poppy.l_elbow_y.goto_position(0, 1, wait=False)
        poppy.r_shoulder_x.goto_position(0, 1, wait=False)
        poppy.r_shoulder_y.goto_position(0, 1, wait=False)
        poppy.r_arm_z.goto_position(0, 1, wait=False)
        poppy.r_elbow_y.goto_position(0, 1, wait=False)

    def update_status_label(self):
        if self.is_running:
            self.robot_status.config(text="Poppy Running", fg="green")
        else:
            self.robot_status.config(text="Poppy Stopped", fg="red")

    def start_robot(self):
        self.poppy = PoppyTorso() # NOTE: We can change the 'vrep' to send commands to the robot.
        # self.poppy = PoppyTorso(simulator='vrep') # NOTE: We can change the 'vrep' to send commands to the robot.
        self.is_running = True
        self.update_status_label()

    # def start_robot(self):
    #     config_path = r'\.venv\Lib\site-packages\poppy_torso\configuration\poppy_torso.json'
    #     self.poppy = PoppyTorso(config_file=config_path, camera='dummy')
    #     self.is_running = True
    #     self.update_status_label()


    def stop_robot(self, poppy):
        if poppy:
            self.is_running = False
            poppy.stop_simulation()
            pypot.vrep.close_all_connections()
            self.update_status_label()


if __name__ == "__main__":
    # Create an instance of the PoppyRobotController class
    controller = PoppyRobotController()
