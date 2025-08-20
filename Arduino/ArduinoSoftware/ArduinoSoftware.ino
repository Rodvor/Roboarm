#include <Servo.h>

const int NUM_SERVOS = 7;
const int servoPins[NUM_SERVOS] = {2, 3, 4, 5, 6, 7, 8};

Servo servos[NUM_SERVOS];
int currentAngles[NUM_SERVOS];
int targetAngles[NUM_SERVOS] = {0};
unsigned int moveIntervals[NUM_SERVOS] = {15}; // ms per degree
bool isMoving[NUM_SERVOS] = {false};
unsigned long lastMoveTimes[NUM_SERVOS] = {0};

// Custom pulse width for extended 270° servo
const int MIN_PULSE = 500;   // 0°
const int MAX_PULSE = 2500;  // 270°
const int MAX_ANGLE = 270;

void writeServoAngle(int id, int angle) {
  if (id < 0 || id >= NUM_SERVOS) return;
  int pulse = map(angle, 0, MAX_ANGLE, MIN_PULSE, MAX_PULSE);
  servos[id].writeMicroseconds(pulse);
}

void moveServoTo(int id, int angle, unsigned int speed) {
  if (id < 0 || id >= NUM_SERVOS) return;
  targetAngles[id] = constrain(angle, 0, MAX_ANGLE);
  moveIntervals[id] = speed;
  isMoving[id] = true;
}

void updateServos() {
  unsigned long now = millis();
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (!isMoving[i]) continue;

    // Always check latest interval (so speed can change mid-motion)
    if (now - lastMoveTimes[i] >= moveIntervals[i]) {
      lastMoveTimes[i] = now;

      if (currentAngles[i] < targetAngles[i]) {
        currentAngles[i]++;
        writeServoAngle(i, currentAngles[i]);
      } else if (currentAngles[i] > targetAngles[i]) {
        currentAngles[i]--;
        writeServoAngle(i, currentAngles[i]);
      } else {
        isMoving[i] = false; // reached target
      }
    }
  }
}

void parseCommand(String cmd) {
  cmd.trim();
  if (cmd.startsWith("MOVE")) {
    int firstSpace = cmd.indexOf(' ');
    int secondSpace = cmd.indexOf(' ', firstSpace + 1);
    int thirdSpace = cmd.indexOf(' ', secondSpace + 1);

    if (firstSpace > 0 && secondSpace > firstSpace && thirdSpace > secondSpace) {
      int servoId = cmd.substring(firstSpace + 1, secondSpace).toInt() - 1;
      int angle   = cmd.substring(secondSpace + 1, thirdSpace).toInt();
      int speed   = cmd.substring(thirdSpace + 1).toInt();

      moveServoTo(servoId, angle, speed);
      Serial.println("OK");
    }
  }
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].attach(servoPins[i], MIN_PULSE, MAX_PULSE);
    currentAngles[i] = 135;
    writeServoAngle(i, currentAngles[i]); // initialize at 0°
  }
  Serial.println("READY");
}

void loop() {
  updateServos();
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    parseCommand(cmd);
  }
}