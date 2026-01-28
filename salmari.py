from ServoController import ServoController
import numpy as np
from kinematics import *
from numpy import pi
from time import sleep
from flask import Flask, render_template_string
import threading

app = Flask(__name__)
busy = threading.Lock()


# All positions
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


# Init servo controller

servo_controller = ServoController()

input("Init arduino?")
servo_controller.auto_detect_arduino()
input("Move?")
servo_controller.third_order_move(resting_pos, 2)


def salmari():

    if not busy.acquire(blocking=False):
        return "Busy pouring... please wait."
    
    threading.Thread(target=pour, daemon=True).start()

    return "Pouring salmari!"

def pour():
    try:
        servo_controller.third_order_move(pre_pour_pos, 2)
        sleep(0.2)
        servo_controller.third_order_move(pouring_pos, [1, 1, 1, 1.2, 1, 1])
        sleep(1) # Pour for one second
        servo_controller.third_order_move(post_pour_pos, [1.4, 2.6, 3, 3, 3, 2])
        sleep(0.2)
        servo_controller.third_order_move(resting_pos, 2)
    finally:
        busy.release()


# Main page
@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Salmari</title>
        <style>
            body {
                margin: 0;
                height: 100vh;
                background: #0a0a0a; /* black slightly brown would be #0a0a05 or similar */
                color: #f5f5f5;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
                text-align: center;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 0.5em;
            }
            p {
                font-size: 1.2em;
                margin-bottom: 2em;
            }
            button {
                padding: 1em 2em;
                font-size: 1.2em;
                border: none;
                border-radius: 12px;
                background: #333300;
                color: #fff;
                cursor: pointer;
                transition: 0.2s;
            }
            button:hover {
                background: #555500;
            }
        </style>
    </head>
    <body>
        <h1>Salmari</h1>
        <p>Please place a glass on the coaster.</p>
        <form action="/salmari" method="get">
            <button type="submit">Order Robo-oil</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)



@app.route("/salmari")
def salmari_route():
    return salmari()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969)