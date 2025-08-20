from flask import Flask, request, render_template
import serial
import glob

possible_ports = glob.glob('/dev/tty.usbserial-*')

if len(possible_ports) == 0:
    print("Arduino not connected!")
    exit()

port = possible_ports[0]

arduino = serial.Serial(port=port, baudrate=115200, timeout=1)
print(f"Detected Arduino at '{port}'")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move")
def move_servo():
    try:
        servo = int(request.args.get("servo", 1))
        angle = int(request.args.get("angle", 90))
        speed = int(request.args.get("speed", 2))
        command = f"MOVE {servo} {angle} {speed}\n"
        arduino.write(command.encode())
        return "OK"
    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969)
