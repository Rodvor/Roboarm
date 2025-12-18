from servo import Servo
import serial
import glob
from time import sleep
import time



class ServoController():

    def __init__(self):

        servo_path = "servos.txt"
        self.arduino = None
        
        # Read servos
        with open(servo_path, "r") as servo_file:
            content = servo_file.read()
        
        content = content.split("\n")

        self.servos = {}

        # Go through each line and setup data structure
        for line in content:

            if line.strip() == "":
                continue

            line = line.split(";")
            servo_name = line[0]
            servo_port = int(line[1])

            new_servo = Servo(servo_name, servo_port)
            new_servo.pulse_range = [int(line[3]), int(line[4])]
            new_servo.config_angles(float(line[5]), [float(line[6]), float(line[7])], int(line[2]), line[8] == "true")
            
            group = line[9]

            if group.lower() == "none":
                self.servos[servo_name] = [new_servo]
                continue

            if not group in self.servos.keys():
                self.servos[group] = [new_servo]
                continue

            self.servos[group] += [new_servo]

    def auto_detect_arduino(self):

        # Auto-detect arduino
        possible_ports = glob.glob('/dev/tty.usbserial-*')

        if len(possible_ports) == 0:
            self.arduino = None
            print("Arduino not connected!")
            return False

        port = possible_ports[0]
        self.arduino = serial.Serial(port, 115200, timeout=1)
        sleep(1)
        print(f"Detected Arduino at '{port}'")

        return True
    
    def set_arduino(self, port):

        self.arduino = serial.Serial(port, 115200, timeout=1)
        sleep(1)
        print(f"Arduino at '{port}'")
    

    def move_servo(self, servo_name, angle, speed):
        """
        Sends: MOVE <servo> <pulse> <speed>
        """

        if self.arduino is None:
            print("No arduino connected: cannot move")
            return False

        if not servo_name in self.servos.keys():
            return False
        
        servos_to_move = self.servos[servo_name]

        for servo in servos_to_move:

            # Set servo properties
            servo.move(angle, speed)

            # Send actual arduino command from servo properties
            cmd = f"MOVE {servo.port} {servo.pulse} {servo.pulse_time}\n"
            self.arduino.write(cmd.encode("utf-8"))
            self.arduino.flush()

    def third_order_step(self, servo_name, t):
        """
        Sends: MOVE <servo> <pulse> <speed>
        """

        if self.arduino is None:
            print("No arduino connected: cannot move")
            return False

        if not servo_name in self.servos.keys():
            return False
        
        servos_to_move = self.servos[servo_name]

        for servo in servos_to_move:

            # Set servo properties
            servo.move_third_order(t)

            # Send actual arduino command from servo properties
            cmd = f"MOVE {servo.port} {servo.pulse} {servo.pulse_time}\n"
            self.arduino.write(cmd.encode("utf-8"))
            self.arduino.flush()

    def third_order_move(self, servo_data, time):
        """
        servo_data = {name : angle}
        """

        for servo_name in servo_data.keys():
            
            for servo in self.servos[servo_name]:

                servo.calculate_third_poly_terms(servo_data[servo_name], time)
        
        my_timer = Timer()

        while my_timer.seconds() <= time:
            
            for servo_name in servo_data.keys():
                
                self.third_order_step(servo_name, my_timer.seconds())

            sleep(0.01)

    def move_servos(self, servo_data):
        """
        servo_data = {name : angle}
        """

        for servo_name in servo_data.keys():

            self.move_servo(servo_name, servo_data[servo_name], -1)
        

    

class Timer:
    def __init__(self):
        self.start = time.time()   # seconds (float)

    def seconds(self):
        return time.time() - self.start

    def milliseconds(self):
        return (time.time() - self.start) * 1000



if __name__ == "__main__":

    servo_controller = ServoController()
    servo_controller.auto_detect_arduino()
    servo_controller.third_order_move({"base": 90}, 2)
    servo_controller.third_order_move({"base": -90}, 2)
    servo_controller.third_order_move({"base": 0}, 2)