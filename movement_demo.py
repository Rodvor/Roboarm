from ServoController import ServoController
import numpy as np
from kinematics import *
from numpy import pi
from time import sleep
from random import randint

def main():

    # Define some positions
    zero = {"base": 0,
                "shoulder": 0,
                "elbow": 0,
                "forearm": 0,
                "wrist": 0,
                "end_effector_base": 0}
    
    resting_pos = {"base": 0,
                "shoulder": 0,
                "elbow": 0,
                "forearm": 90,
                "wrist": -90,
                "end_effector_base": 90}
    
    pos1 = {"base": 0,
                "shoulder": 25,
                "elbow": -90,
                "forearm": 90,
                "wrist": -90,
                "end_effector_base": 25}
    
    play_poses = [pos1]
    
    # Init servo controller
    servo_controller = ServoController()

    # Ask user to move?
    input("[Input] Move to resting position?")
    servo_controller.auto_detect_arduino()

    robot = my_robot()

    while True:
        
        # Return to default pos
        servo_controller.third_order_move(resting_pos, 3)

        # Continue? 
        if input("[Input] Move?") != "": break

        print("[Robo] Moving...")
        
        # Move through all listed poses, random time
        for pos in play_poses:

            move_time = randint(2, 5)
            servo_controller.third_order_move(pos, move_time)
        
        print("[Robo] Returning to rest...")


    # Loop exit -> Reset

    print("[Robo] Resetting to zero...")

    servo_controller.third_order_move(zero, 2)

    print("[Robo] Done! Quitting...")




if __name__ == "__main__":
    main()