#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_BMP3XX.h>
#include <SparkFun_Ublox_Arduino_Library.h>
#include <Servo.h>

#define LED_GATE_PIN 21 // Example: Connect MOSFET gate to GP1
#define SERVO_SIGNAL_PIN 20 // Example: Connect servo signal to GP0

#define BUZZER_GATE_PIN 22 // Example: Connect MOSFET gate to GP1
#define SERVO_SIGNAL_PIN 20 // Example: Connect servo signal to GP0


void setup() {
  Serial.begin(9600);
  pinMode(LED_GATE_PIN, OUTPUT); // Set MOSFET control pin as output
  digitalWrite(LED_GATE_PIN, LOW); // Ensure MOSFET is initially off

  pinMode(BUZZER_GATE_PIN, OUTPUT); // Set MOSFET control pin as output
  digitalWrite(BUZZER_GATE_PIN, LOW); // Ensure MOSFET is initially off
}

void loop() {
if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove whitespace

    if (command == "1") {
      digitalWrite(LED_GATE_PIN, HIGH);
      Serial.println("1");
    } else if (command == "0") {
      digitalWrite(LED_GATE_PIN, LOW);
      Serial.println("0");
    }
  }

if (Serial.available()) {
    String commandbuzz = Serial.readStringUntil('\n');
    commandbuzz.trim(); // Remove whitespace

    if (commandbuzz == "3") {
      digitalWrite(BUZZER_GATE_PIN, HIGH);
      Serial.println("3");
    } else if (commandbuzz == "4") {
      digitalWrite(BUZZER_GATE_PIN, LOW);
      Serial.println("4");
    }
  }
}

