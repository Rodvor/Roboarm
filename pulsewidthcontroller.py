import serial
import glob

possible_ports = glob.glob('/dev/tty.usbserial-*')

if len(possible_ports) == 0:
    print("Arduino not connected!")
    exit()

port = possible_ports[0]
print(f"Detected Arduino at '{port}'")

BAUD = 115200

def send_move(arduino, servo, pulse, speed):
    """
    Sends: MOVE <servo> <pulse> <speed>
    Servo counting starts at 1 (same as your Arduino code).
    """
    cmd = f"MOVE {servo} {pulse} {speed}\n"
    arduino.write(cmd.encode("utf-8"))
    arduino.flush()
    print("Sent:", cmd.strip())

# -----------------------------

if __name__ == "__main__":

    while True:

        porttt = int(input("Enter port: "))
        pulse = int(input("Enter pulse: "))
        speed = int(input("Enter speed: "))

        arduino = serial.Serial(port, 115200, timeout=1)

        print("Arduino says:", arduino.readline().decode().strip())

        # Example: move servo 4 to 1500 µs at 10 ms per µs
        send_move(arduino, servo=porttt, pulse=pulse, speed=speed)

        # Listen for Arduino reply
        response = arduino.readline().decode().strip()
        print("Arduino reply:", response)

    ser.close()