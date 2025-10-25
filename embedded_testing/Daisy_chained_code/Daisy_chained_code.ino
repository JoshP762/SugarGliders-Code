#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_BMP3XX.h>
#include <SparkFun_Ublox_Arduino_Library.h>
#include <Servo.h>
//#include <XBee.h>
#include <SoftwareSerial.h>
#include <string.h>

// I2C Pins for Pico (GP16 = SDA, GP17 = SCL)
const int I2CSDA = 16;
const int I2CSCL = 17;

static int packetCount = 0; // Move this outside loop

bool telemetryActive = true;
bool landingActionsTriggered = false;

const int voltagePin = 26; // GP26 = ADC0

#define MOSFET_GATE_PIN 27 // Example: Connect MOSFET gate to GP1  For Servo
#define SERVO_SIGNAL_PIN 20 // Example: Connect servo signal to GP0

#define LED_GATE_PIN 21 // Example: Connect MOSFET gate to GP1

#define BUZZER_GATE_PIN 22 // Example: Connect MOSFET gate to GP1

SoftwareSerial openLog(1,0);

int ledPin=LED_BUILTIN;

String plState = "RELEASED"; // Default state

bool servoDeployed = false;
unsigned long servoStartTime = 0;
bool servoActive = false;
Servo myservo;

/*
#define MOSFET_GATE_PIN 21 // Example: Connect MOSFET gate to GP1
#define SERVO_SIGNAL_PIN 20 // Example: Connect servo signal to GP0
Servo myservo; // Create a servo object
*/

// Sensor objects
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
Adafruit_BMP3XX bmp;
SFE_UBLOX_GPS gps;

void setup() {
  Serial.begin(9600);
  Wire.setSDA(I2CSDA);
  Wire.setSCL(I2CSCL);
  Wire.begin();

  Serial1.setTX(12);
  Serial1.setRX(13);
  Serial1.begin(9600);

  pinMode(ledPin,OUTPUT);
  openLog.begin(9600);   


  pinMode(MOSFET_GATE_PIN, OUTPUT); // Set MOSFET control pin as output
  digitalWrite(MOSFET_GATE_PIN, LOW); // Ensure MOSFET is initially off
  myservo.attach(SERVO_SIGNAL_PIN);   // Attach servo signal



  pinMode(LED_GATE_PIN, OUTPUT); // Set MOSFET control pin as output
  digitalWrite(LED_GATE_PIN, LOW); // Ensure MOSFET is initially off

  pinMode(BUZZER_GATE_PIN, OUTPUT); // Set MOSFET control pin as output
  digitalWrite(BUZZER_GATE_PIN, LOW); // Ensure MOSFET is initially off


  Serial.println("Initializing sensors...");

  // BNO055
  if (!bno.begin()) {
    Serial.println("BNO055 not detected. Check wiring.");
    //while (1);
  }

  // BMP388
  if (!bmp.begin_I2C()) {
    Serial.println("BMP388 not detected. Check wiring.");
    //while (1);
  }
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_7);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);

  // ZOE-M8Q
  if (!gps.begin()) {
    Serial.println("ZOE-M8Q not detected. Check wiring.");
    //while (1);
  }
  gps.setI2COutput(COM_TYPE_NMEA); // Optional: UBX or NMEA
  gps.setNMEAOutputPort(Serial1);   // Pipe NMEA to Serial

  delay(1000);

  /* Mosfets
  pinMode(MOSFET_GATE_PIN, OUTPUT); // Set MOSFET control pin as output
  digitalWrite(MOSFET_GATE_PIN, LOW); // Ensure MOSFET is initially off
  myservo.attach(SERVO_SIGNAL_PIN);
  */
}

void loop() {
  // BNO055 Orientation
  sensors_event_t orientation, gyro, accel, gravity;
  bno.getEvent(&orientation, Adafruit_BNO055::VECTOR_EULER);
  bno.getEvent(&gyro, Adafruit_BNO055::VECTOR_GYROSCOPE);
  bno.getEvent(&accel, Adafruit_BNO055::VECTOR_ACCELEROMETER);
  bno.getEvent(&gravity, Adafruit_BNO055::VECTOR_GRAVITY);

  Serial1.print("Orient: ");
  Serial1.print(orientation.orientation.x); Serial1.print(", ");
  Serial1.print(orientation.orientation.y); Serial1.print(", ");
  Serial1.println(orientation.orientation.z);

  Serial1.print("GYRO_R = ");
  Serial1.print(gyro.gyro.x); Serial1.print("\n");

  Serial1.print("GYRO_P = ");
  Serial1.print(gyro.gyro.y); Serial1.print("\n");
  
  Serial1.print("GYRO_Y = ");
  Serial1.println(gyro.gyro.z);

  Serial1.print("Accel = ");
  Serial1.println(accel.acceleration.z);



  // Voltage
  int raw = analogRead(voltagePin); // 0–4095 for 12-bit ADC 
  float voltage = 2*((raw * (3.3 / 1023.0))*5); // Convert to volts
  // float battery=voltage/2.0;


  Serial1.print("Voltage = ");
  Serial1.println(voltage, 2); // Print with 2 decimal places

  delay(250);


  // BMP388 Pressure & Altitude
  if (bmp.performReading()) {
    float altitude = bmp.readAltitude(1013.25);
    Serial1.print("Pressure = ");
    Serial1.print(bmp.pressure / 100.0); Serial1.print(" hPa\t");
    Serial1.print("\nAltitude = ");
    Serial1.print(bmp.readAltitude(1013.25)); Serial1.println(" m");
    Serial1.print("Temperature = "); Serial1.print(bmp.temperature);
    Serial1.println(" *C");

  // Servo

  // Release (0 Degrees)
   if (altitude > 520 && !servoDeployed) {  // Should be 520 m
    digitalWrite(MOSFET_GATE_PIN, HIGH);
    myservo.write(0);
    plState = "R";
    servoStartTime = millis();
    servoActive = true;
    servoDeployed = true;
  }
}
  // Lock (180 Degrees)
  if(Serial1.available()){
    String command = Serial1.readStringUntil('\n');
    command.trim(); // Remove whitespace
    if (command == "SERVO_LOCK") {
      digitalWrite(MOSFET_GATE_PIN, HIGH); // Power the servo
      myservo.write(180);
      plState="N";                  // Move to locked position
      Serial.println("SERVO_LOCK");
      delay(500);                          // Hold position
      digitalWrite(MOSFET_GATE_PIN, LOW);  // Cut power
    }

  // Release (0 Degrees)
    else if (command == "SERVO_RELEASE") {
      digitalWrite(MOSFET_GATE_PIN, HIGH); // Power the servo
      myservo.write(0);
      plState = "R";                  // Move to locked position
      Serial.println("SERVO_RELEASE");
      delay(500);                          // Hold position
      digitalWrite(MOSFET_GATE_PIN, LOW);  // Cut power
    }
}


// LED and BUZZER code
if (Serial.available()) {
  String command = Serial.readStringUntil('\n');
  command.trim();

  if (command == "1") {
    digitalWrite(LED_GATE_PIN, HIGH);
    Serial.println("LED ON");
  } else if (command == "0") {
    digitalWrite(LED_GATE_PIN, LOW);
    Serial.println("LED OFF");
  } else if (command == "3") {
    digitalWrite(BUZZER_GATE_PIN, HIGH);
    Serial.println("BUZZER ON");
  } else if (command == "4") {
    digitalWrite(BUZZER_GATE_PIN, LOW);
    Serial.println("BUZZER OFF");
  }
}



float altitude = bmp.readAltitude(1013.25);

  // States
String flightState = "";

if (altitude < 50) {
  flightState = "LAUNCH_READY";
}
else if (altitude >= 50 && altitude < 520) {
  flightState = "ASCENT";
}
else if (servoActive) {
  flightState = "SEPARATE";

}
else if (altitude >= 520) {
  flightState = "DESCENT";
}
else {
  flightState = "LANDED";
}

if (flightState == "LANDED" && !landingActionsTriggered) {
    telemetryActive = false;
    digitalWrite(LED_GATE_PIN, HIGH);
    digitalWrite(BUZZER_GATE_PIN, HIGH);
    landingActionsTriggered = true;
    Serial1.println("Landing detected — telemetry stopped, LED and buzzer activated.");
  }


  Serial1.print("SW_STATE = ");
  Serial1.println(flightState);

  Serial1.print("PL_STATE = ");
  Serial1.println(plState);


if (servoActive && millis() - servoStartTime > 500) {
  digitalWrite(MOSFET_GATE_PIN, LOW);
  servoActive = false;
}

  // ZOE-M8Q GPS
  gps.checkUblox(); // Process incoming GPS data

  if (gps.getFixType() > 1) { // 2D or 3D fix
  Serial1.print("Latitude = ");
  Serial1.println(gps.getLatitude() / 10000000.0, 7);
  Serial1.print("Longitude = ");
  Serial1.println(gps.getLongitude() / 10000000.0, 7);
  }  
  else {
  Serial1.println("Waiting for GPS fix...");
  }

  Serial1.print("Packet_Count = ");
  Serial1.println(packetCount++);

  // XBee telemetry format
  if(telemetryActive){
    openLog.print("2,");
    openLog.print(millis() / 1000.0); openLog.print(",");
    openLog.print(packetCount); openLog.print(",");
    openLog.print(flightState); openLog.print(",");
    openLog.print(plState); openLog.print(",");
    openLog.print(bmp.readAltitude(1013.25)); openLog.print(",");
    openLog.print(bmp.temperature); openLog.print(",");
    openLog.print(voltage, 2); openLog.print(","); 
    openLog.print(gps.getLatitude() / 10000000.0, 4); openLog.print(","); // GPS_LATITUDE
    openLog.print(gps.getLongitude() / 10000000.0, 4); openLog.print(","); // GPS_LONGITUDE
    openLog.print(gyro.gyro.x); openLog.print(","); 
    openLog.print(gyro.gyro.y); openLog.print(",");
    openLog.print(gyro.gyro.z); openLog.print(",,"); 
    openLog.println(accel.acceleration.z);
  }


  delay(250);

  /* Mosfet
  // Turn on the MOSFET to power the servo
  digitalWrite(MOSFET_GATE_PIN, HIGH);
  delay(100); // Allow time for power to stabilize

  // Control the servo
  for (int angle = 0; angle <= 180; angle += 1) {
    myservo.write(angle);
    delay(15);
  }
  delay(500);

  // Turn off the MOSFET to cut power to the servo
  digitalWrite(MOSFET_GATE_PIN, LOW);
  delay(1000); // Keep servo off for a duration

  */
}