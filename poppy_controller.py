import tkinter as tk
import time
import pypot
from pypot.creatures import PoppyHumanoid


class PoppyRobotController:
    def __init__(self):
        self.window = tk.Tk()
        self.poppy = PoppyHumanoid(simulator='vrep')

        # Create buttons to control the robot
        self.create_buttons()

        self.window.mainloop()

    def create_buttons(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack(side="top")
        forward_button = tk.Button(
            button_frame, text="Move Forward", command=lambda: self.move_forward(self.poppy))
        forward_button.pack(side="left")
        backward_button = tk.Button(
            button_frame, text="Move Backward", command=lambda: self.move_backward(self.poppy))
        backward_button.pack(side="left")
        left_button = tk.Button(
            button_frame, text="Turn Left", command=lambda: self.turn_left(self.poppy))
        left_button.pack(side="left")
        right_button = tk.Button(
            button_frame, text="Turn Right", command=lambda: self.turn_right(self.poppy))
        right_button.pack(side="left")
        arm_up_button = tk.Button(
            button_frame, text="Raise Arm", command=lambda: self.raise_arm(self.poppy))
        arm_up_button.pack(side="left")
        arm_down_button = tk.Button(
            button_frame, text="Lower Arm", command=lambda: self.lower_arm(self.poppy))
        arm_down_button.pack(side="left")
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

    def move_forward(self, poppy):
        # Code to move the robot forward
        print("Moving forward...")
        # TODO: write the code to move the robot forward

    def move_backward(self, poppy):
        # Code to move the robot backward
        print("Moving backward...")
        # TODO: write the code to move the robot forward

    def turn_left(self, poppy):
        # Code to turn the robot left
        print("Turning left...")
        # TODO: write the code to move the robot forward

    def turn_right(self, poppy):
        # Code to turn the robot right
        print("Turning right...")
        # TODO: write the code to move the robot forward

    def raise_arm(self, poppy):
        # Code to raise the robot's arm
        print("Raising arm...")
        # TODO: write the code to move the robot forward

    def lower_arm(self, poppy):
        # Code to lower the robot's arm
        print("Lowering arm...")
        # TODO: write the code to move the robot forward

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
        # TODO: dance the YMCA
        pass

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
        # TODO: Implement move_m function
        pass

    def move_c(self, poppy, speed):
        # TODO: Implement move_c function
        pass

    def move_a(self, poppy, speed):
        # TODO: Implement move_a function
        pass

    def start_position(self, poppy):
        # Move robot to start position
        print("Moving to start position...")
        poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        poppy.l_shoulder_y.goto_position(0, 1, wait=False)
        poppy.l_arm_z.goto_position(0, 1, wait=False)
        poppy.l_elbow_y.goto_position(0, 1, wait=False)

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
