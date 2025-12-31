from ServoController import ServoController
import numpy as np
from kinematics import *
from numpy import pi
from time import sleep

def main():

    full_test = True

    zero = {"base": 0,
                "shoulder": 0,
                "elbow": 0,
                "forearm": 0,
                "wrist": 0,
                "end_effector_base": 0}

    if full_test:

        first = {"base": 0,
                "shoulder": 60,
                "elbow": -90,
                "forearm": 90,
                "wrist": 90,
                "end_effector_base": 90
                }


        second = {"base": 0,
                "shoulder": -60,
                "elbow" : -70,
                "forearm": -90,
                "wrist": -90,
                "end_effector_base": -90}
        

    
    else:

        first = {
            "elbow": 90
        }
        second = {
            "elbow": -90
        }



    servo_controller = ServoController()

    for servo_group in servo_controller.servos.values():

        for servo in servo_group:

            print(f"> {servo.name} in port {servo.port} with zero pulse: {servo.pulse}")

    input("Start moving?")

    servo_controller.auto_detect_arduino()
    servo_controller.third_order_move(zero, 2)

    print(servo_controller.servos["elbow"][0].pulse)
    
    input("Press enter to continue")

    inverse_kinematics_test(servo_controller)

    return
    servo_controller.third_order_move(first, 5)
    servo_controller.third_order_move(second, 5)
    servo_controller.third_order_move(zero, 5)    
    

def inverse_kinematics_test(servo_controller: ServoController):

    zero = {"base": 0,
            "shoulder": 0,
            "elbow": 0,
            "forearm": 0,
            "wrist": 0,
            "end_effector_base": 0}

    orientation = [zero["forearm"], zero["wrist"], 0]

    robot = my_robot()
    previous_coordinates = [300, 0, 500, orientation[0], orientation[1], orientation[2]]

    inverse_kinematics_move(servo_controller, robot, cartesian_to_matrix(previous_coordinates), 3)

    while True:

        try:
            x = int(input("x: "))
            y = int(input("y: "))
            z = int(input("z: "))
            a = zero["forearm"]
            b = zero["wrist"]
            g = x + y

        except:
            break
        
        coordinates = [x, y, z, a, b, g]

        for i in range(100):
            
            das_interpol = interpolate(previous_coordinates, coordinates, i/100)

            inverse_kinematics_move(servo_controller, robot, cartesian_to_matrix(das_interpol))

            sleep(0.05)
        
        previous_coordinates = coordinates

    

    servo_controller.third_order_move(zero, 4)


def inverse_kinematics_move(servo_controller, robot, coordinates, time = 0):

    q = robot.ikine(coordinates)
    servo_data = convert_to_servo_data(q.evalf(10))
    #print_servo_data(servo_data)

    if time == 0:
        servo_controller.move_servos(servo_data)
    else:
        servo_controller.third_order_move(servo_data, time)


def print_servo_data(servo_data):

    for servo in servo_data.keys():

        print(f"> {servo}: {servo_data[servo]}°")

def interpolate(start, end, t):
    """
    Linearly interpolate between start and end by fraction t (0 to 1),
    returning a list of floats.
    """
    return [s + (e - s) * t for s, e in zip(start, end)]




if __name__ == "__main__":
    main()
