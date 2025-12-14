import time
import requests

API_URL = "http://localhost:6969/move"   # change if needed

# Adjustable speed
MOVE_SPEED = 100

def send_move(servo, angle, speed):
    params = {
        "servo": servo,
        "angle": angle,
        "speed": speed
    }
    try:
        r = requests.get(API_URL, params=params, timeout=2)
        print(f"Sent servo {servo} -> {angle}° at speed {speed}: {r.text}")
    except Exception as e:
        print(f"Error sending command: {e}")

def main_loop():
    while True:
        # Time = 0
        send_move(1, 135, MOVE_SPEED)
        send_move(2, 135, MOVE_SPEED)

        time.sleep(10)

        # Time = 10 s
        send_move(1, 45, MOVE_SPEED)
        send_move(2, 225, MOVE_SPEED)

        time.sleep(10)


if __name__ == "__main__":
    main_loop()
