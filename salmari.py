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
                "forearm": 90,
                "wrist": -90,
                "end_effector_base": 90}
    
    default_pos = {"base": -21,
                "shoulder": 25,
                "elbow": 50,
                "forearm": 90,
                "wrist": -90,
                "end_effector_base": 25}

    pre_pour_pos = {"base": -33,
                "shoulder": 25,
                "elbow": 60,
                "forearm": 10,
                "wrist": -90,
                "end_effector_base": 0}

    post_pour_pos = {"base": -30,
                "shoulder": 20,
                "elbow": 85,
                "forearm": 35,
                "wrist": -90,
                "end_effector_base": -5}

    pouring_pos = {"base": -18,
                "shoulder": 25,
                "elbow": 60,
                "forearm": -41,
                "wrist": -90,
                "end_effector_base": 0}
    
    servo_controller = ServoController()

    input("Init arduino?")
    servo_controller.auto_detect_arduino()
    input("Move?")
    servo_controller.third_order_move(resting_pos, 2)
    #servo_controller.third_order_move(default_pos, 2)

    robot = my_robot()

    while True:

        try:
            int(input("Pour?"))
        except:
            break
        servo_controller.third_order_move(pre_pour_pos, 2)
        sleep(1)
        servo_controller.third_order_move(pouring_pos, [1, 1, 1, 1.2, 1, 1])
        sleep(1)
        servo_controller.third_order_move(post_pour_pos, [1.4, 2.6, 3, 3, 3, 2])
        sleep(1)
        servo_controller.third_order_move(resting_pos, 2)
        sleep(1)
        

    
    input("Press enter to continue")

    servo_controller.third_order_move(zero, 2)




if __name__ == "__main__":
    main()