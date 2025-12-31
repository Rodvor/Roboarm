from ServoController import ServoController
import numpy as np
from kinematics import *
from numpy import pi
from time import sleep

def main():

    zero = {"base": 0,
                "shoulder": 0,
                "elbow": 0,
                "forearm": 0,
                "wrist": 0,
                "end_effector_base": 0}
    
    resting_pos = {"base": 0,
                "shoulder": 0,
                "elbow": 0,
                "forearm": -90,
                "wrist": 90,
                "end_effector_base": -90}
    
    default_pos = {"base": 0,
                "shoulder": -25,
                "elbow": 90,
                "forearm": -90,
                "wrist": 90,
                "end_effector_base": -25}
    
    servo_controller = ServoController()

    input("Start moving?")
    servo_controller.auto_detect_arduino()
    servo_controller.third_order_move(resting_pos, 2)
    servo_controller.third_order_move(default_pos, 2)

    robot = my_robot()

    while True:

        try:
            print("-----------------------------")
            x = int(input("x: "))
            y = int(input("y: "))
            z = int(input("z: "))
        except:
            break

        thetas = robot.no_wrist_ikine([x,y,z])
        new_base = thetas[0] * 180/pi
        new_shoulder = thetas[1] * 180/pi
        new_elbow = thetas[2] * 180/pi

        new_pos = {"base": new_base,
                "shoulder": new_shoulder,
                "elbow": new_elbow,
                "forearm": -90,
                "wrist": 90,
                "end_effector_base": -90 + new_shoulder + new_elbow}

        print(new_pos)

        if input("are you sure: ") != "":
            continue
        

        servo_controller.third_order_move(new_pos, 2)




    
    input("Press enter to continue")

    servo_controller.third_order_move(zero, 2)




if __name__ == "__main__":
    main()