import tkinter as tk
import time
import pypot
from pypot.creatures import PoppyHumanoid


class PoppyRobotController:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Poppy Robot Controller")
        self.poppy = PoppyHumanoid(simulator='vrep')

        # Create buttons to control the robot
        self.create_buttons()

        self.window.mainloop()

    def create_buttons(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack(side="top")
        start_button = tk.Button(
            button_frame, text="Start Position", command=lambda: self.start_position(self.poppy))
        start_button.pack(side="left")
        wave_button = tk.Button(
            button_frame, text="Wave Hand", command=lambda: self.wave_hand(self.poppy))
        wave_button.pack(side="left")
        dance_button = tk.Button(
            button_frame, text="Dance", command=lambda: self.dance_ymca(self.poppy))
        dance_button.pack(side="left")
        y_button = tk.Button(button_frame, text="Y",
                             command=lambda: self.move_y(self.poppy, 1))
        y_button.pack(side=tk.LEFT)
        m_button = tk.Button(button_frame, text="M",
                             command=lambda: self.move_m(self.poppy, 1))
        m_button.pack(side=tk.LEFT)
        c_button = tk.Button(button_frame, text="C",
                             command=lambda: self.move_c(self.poppy, 1))
        c_button.pack(side=tk.LEFT)
        a_button = tk.Button(button_frame, text="A",
                             command=lambda: self.move_a(self.poppy, 1))
        a_button.pack(side=tk.LEFT)

        # Create buttons to start and stop the robot
        start_button = tk.Button(
            self.window, text="Start Robot", command=self.start_robot)
        start_button.pack(side="left", padx=10, pady=10)
        stop_button = tk.Button(
            self.window, text="Stop Robot", command=lambda: self.stop_robot(self.poppy))
        stop_button.pack(side="left", padx=10, pady=10)

    def wave_hand(self, poppy):
        # Code to make the robot wave its hand
        print("Waving hand...")
        # TODO: write the code to move the robot forward
        if poppy is not None:
            # Move arm back to starting position
            poppy.l_shoulder_x.goto_position(0, 1, wait=False)
            poppy.l_shoulder_y.goto_position(0, 1, wait=False)
            poppy.l_arm_z.goto_position(0, 1, wait=False)
            poppy.l_elbow_y.goto_position(0, 1, wait=False)

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
            poppy.l_shoulder_x.goto_position(0, 1, wait=False)
            poppy.l_shoulder_y.goto_position(0, 1, wait=False)
            poppy.l_arm_z.goto_position(0, 1, wait=False)
            poppy.l_elbow_y.goto_position(0, 1, wait=False)

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
        poppy.l_shoulder_x.goto_position(10, speed, wait=False)
        poppy.l_shoulder_y.goto_position(0, speed, wait=False)
        poppy.l_arm_z.goto_position(90, speed, wait=False)
        poppy.l_elbow_y.goto_position(-50, speed, wait=False)
        poppy.r_shoulder_x.goto_position(-160, speed, wait=False)
        poppy.r_shoulder_y.goto_position(0, speed, wait=False)
        poppy.r_arm_z.goto_position(-90, speed, wait=False)
        poppy.r_elbow_y.goto_position(-70, speed, wait=False)
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

    def start_robot(self):
        # Code to start the robot
        print("Starting robot...")
        # Start the robot simulation - When the robot is contructed, can change this to control the real robot
        self.poppy = PoppyHumanoid(simulator='vrep')

    def stop_robot(self, poppy):
        # Code to stop the robot
        print("Stopping robot...")
        poppy.stop_simulation()
        pypot.vrep.close_all_connections()


if __name__ == "__main__":
    # Create an instance of the PoppyRobotController class
    controller = PoppyRobotController()
