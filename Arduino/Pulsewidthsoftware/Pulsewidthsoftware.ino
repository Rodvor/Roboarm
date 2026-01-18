#include <Servo.h>

const int NUM_SERVOS = 10;
const int servoPins[NUM_SERVOS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};

Servo servos[NUM_SERVOS];
int currentPulses[NUM_SERVOS];          // current microsecond command
int targetPulses[NUM_SERVOS] = {0};     // target microsecond command
unsigned int moveIntervals[NUM_SERVOS] = {15}; // ms per µs
bool isMoving[NUM_SERVOS] = {false};
unsigned long lastMoveTimes[NUM_SERVOS] = {0};
const int servoZeroPulse[NUM_SERVOS] = {1574, 1500, 1444, 1552, 1440, 1500, 1515, 1456, 500, 1500};

// Valid servo pulse range
const int MIN_PULSE = 500;
const int MAX_PULSE = 2500;

void writeServoPulse(int id, int pulse) {
  if (id < 0 || id >= NUM_SERVOS) return;
  servos[id].writeMicroseconds(pulse);
}

void moveServoTo(int id, int pulse, unsigned int speed) {
  if (id < 0 || id >= NUM_SERVOS) return;

  pulse = constrain(pulse, MIN_PULSE, MAX_PULSE);

  targetPulses[id] = pulse;
  moveIntervals[id] = speed;
  isMoving[id] = true;
}

void updateServos() {
  unsigned long now = millis();

  for (int i = 0; i < NUM_SERVOS; i++) {
    if (!isMoving[i]) continue;

    if (now - lastMoveTimes[i] >= moveIntervals[i]) {
      lastMoveTimes[i] = now;

      if (currentPulses[i] < targetPulses[i]) {
        currentPulses[i]++;
        writeServoPulse(i, currentPulses[i]);
      } else if (currentPulses[i] > targetPulses[i]) {
        currentPulses[i]--;
        writeServoPulse(i, currentPulses[i]);
      } else {
        isMoving[i] = false; // Reached target
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
      int pulse   = cmd.substring(secondSpace + 1, thirdSpace).toInt();
      int speed   = cmd.substring(thirdSpace + 1).toInt();

      moveServoTo(servoId, pulse, speed);
      Serial.println("OK");
    }
  }
}

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].attach(servoPins[i], MIN_PULSE, MAX_PULSE);

    currentPulses[i] = servoZeroPulse[i]; // centre approx
    writeServoPulse(i, currentPulses[i]);
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
