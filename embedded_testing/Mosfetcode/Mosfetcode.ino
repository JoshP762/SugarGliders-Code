#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_BMP3XX.h>
#include <SparkFun_Ublox_Arduino_Library.h>
#include <Servo.h>

#define MOSFET_GATE_PIN 21 // Example: Connect MOSFET gate to GP1
#define SERVO_SIGNAL_PIN 20 // Example: Connect servo signal to GP0

void setup() {
  pinMode(MOSFET_GATE_PIN, OUTPUT); // Set MOSFET control pin as output
  digitalWrite(MOSFET_GATE_PIN, LOW); // Ensure MOSFET is initially off
}

void loop() {

// Turn on the MOSFET to power the servo
  digitalWrite(MOSFET_GATE_PIN, HIGH);
  delay(100); // Allow time for power to stabilize

  // Turn off the MOSFET to cut power to the servo
  digitalWrite(MOSFET_GATE_PIN, LOW);
  delay(1000); // Keep servo off for a duration


}
