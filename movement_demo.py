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
                "shoulder": -30,
                "elbow": 90,
                "forearm": 0,
                "wrist": -30,
                "end_effector_base": 90}
    
    pos1 = {"base": 20,
                "shoulder": 30,
                "elbow": 30,
                "forearm": 40,
                "wrist": -30,
                "end_effector_base": 50}
    
    pos2 = {"base": -45,
                "shoulder": 20,
                "elbow": 55,
                "forearm": 74,
                "wrist": -3,
                "end_effector_base": 20}
    
    pos3 = {"base": 30,
                "shoulder": -50,
                "elbow": 90,
                "forearm": 83,
                "wrist": 90,
                "end_effector_base": -55}
    
    play_poses = [pos1, pos2, pos3]
    
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