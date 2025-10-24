#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_BMP3XX.h>
#include <SparkFun_Ublox_Arduino_Library.h>
#include <Servo.h>

// I2C Pins for Pico (GP16 = SDA, GP17 = SCL)
const int I2CSDA = 16;
const int I2CSCL = 17;

const int voltagePin = 26; // GP26 = ADC0

#define MOSFET_GATE_PIN 27 // Example: Connect MOSFET gate to GP1  For Servo
#define SERVO_SIGNAL_PIN 20 // Example: Connect servo signal to GP0

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

  pinMode(MOSFET_GATE_PIN, OUTPUT); // Set MOSFET control pin as output
  digitalWrite(MOSFET_GATE_PIN, LOW); // Ensure MOSFET is initially off
  myservo.attach(SERVO_SIGNAL_PIN);   // Attach servo signal


  Serial.println("Initializing sensors...");

  // BNO055
  if (!bno.begin()) {
    Serial.println("BNO055 not detected. Check wiring.");
    while (1);
  }

  // BMP388
  if (!bmp.begin_I2C()) {
    Serial.println("BMP388 not detected. Check wiring.");
    while (1);
  }
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_7);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);


  
  // ZOE-M8Q
  if (!gps.begin()) {
    Serial.println("ZOE-M8Q not detected. Check wiring.");
    while (1);
  }
  gps.setI2COutput(COM_TYPE_NMEA); // Optional: UBX or NMEA
  gps.setNMEAOutputPort(Serial);   // Pipe NMEA to Serial

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

  Serial.print("Orient: ");
  Serial.print(orientation.orientation.x); Serial.print(", ");
  Serial.print(orientation.orientation.y); Serial.print(", ");
  Serial.println(orientation.orientation.z);

  Serial.print("GYRO_R = ");
  Serial.print(gyro.gyro.x); Serial.print("\n");

  Serial.print("GYRO_P = ");
  Serial.print(gyro.gyro.y); Serial.print("\n");
  
  Serial.print("GYRO_Y = ");
  Serial.println(gyro.gyro.z);

  Serial.print("Accel = ");
  Serial.println(accel.acceleration.z);


  // Voltage
  int raw = analogRead(voltagePin); // 0–4095 for 12-bit ADC
  float voltage = (raw * (3.3 / 1023.0))*5; // Convert to volts
  float battery=voltage/2.0;


  Serial.print("Voltage = ");
  Serial.println(voltage, 2); // Print with 2 decimal places

  delay(250);


  // BMP388 Pressure & Altitude
  if (bmp.performReading()) {
    float altitude = bmp.readAltitude(1013.25);
    Serial.print("Pressure = ");
    Serial.print(bmp.pressure / 100.0); Serial.print(" hPa\t");
    Serial.print("\nAltitude = ");
    Serial.print(bmp.readAltitude(1013.25)); Serial.println(" m");
    Serial.print("Temperature = "); Serial.print(bmp.temperature);
    Serial.println(" *C");

  // Servo

  // Release (0 Degrees)
   if (altitude > 110 && !servoDeployed) {  // Should be 520 m
    Serial.println("SW_State = 2");
    digitalWrite(MOSFET_GATE_PIN, HIGH);
    myservo.write(0);
    servoStartTime = millis();
    servoActive = true;
    servoDeployed = true;
  }
}
  // Lock (180 Degrees)
  if(Serial.available()){
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove whitespace
    if (command == "SERVO_LOCK") {
      digitalWrite(MOSFET_GATE_PIN, HIGH); // Power the servo
      myservo.write(180);                  // Move to locked position
      Serial.println("SERVO_LOCK");
      delay(500);                          // Hold position
      digitalWrite(MOSFET_GATE_PIN, LOW);  // Cut power
    }

  // Release (0 Degrees)
    else if (command == "SERVO_RELEASE") {
      digitalWrite(MOSFET_GATE_PIN, HIGH); // Power the servo
      myservo.write(0);                  // Move to locked position
      Serial.println("SERVO_RELEASE");
      delay(500);                          // Hold position
      digitalWrite(MOSFET_GATE_PIN, LOW);  // Cut power
    }
}

// States




if (servoActive && millis() - servoStartTime > 500) {
  digitalWrite(MOSFET_GATE_PIN, LOW);
  servoActive = false;
}

  // ZOE-M8Q GPS
  gps.checkUblox(); // Process incoming GPS data

  if (gps.getFixType() > 1) { // 2D or 3D fix
  Serial.print("Latitude = ");
  Serial.println(gps.getLatitude() / 10000000.0, 7);
  Serial.print("Longitude = ");
  Serial.println(gps.getLongitude() / 10000000.0, 7);
  }  
  else {
  Serial.println("Waiting for GPS fix...");
  }

  static int packetCount = 0;
  Serial.print("Packet_Count = ");
  Serial.println(packetCount++);

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