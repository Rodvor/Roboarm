from ServoController import ServoController


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

    servo_controller.third_order_move(first, 5)
    servo_controller.third_order_move(second, 5)
    servo_controller.third_order_move(zero, 5)    
    





if __name__ == "__main__":
    main()
