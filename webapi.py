from flask import Flask, render_template, request, jsonify
from ServoController import ServoController

app = Flask(__name__)

servo_controller = ServoController()
servo_controller.auto_detect_arduino()

SERVO_NAMES = [
    "base",
    "shoulder",
    "elbow",
    "forearm",
    "wrist",
    "end_effector_base"
]


@app.route("/")
def index():
    return render_template("index.html", servos=SERVO_NAMES)


@app.route("/move", methods=["POST"])
def move():
    data = request.json

    angles = {}
    for name in SERVO_NAMES:
        if name in data:
            angles[name] = int(data[name])

    duration = float(data.get("duration", 3))

    servo_controller.third_order_move(angles, duration)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969, debug=False)
