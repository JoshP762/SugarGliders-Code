#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_BMP3XX.h>
#include <SparkFun_Ublox_Arduino_Library.h>

// I2C Pins for Pico (GP16 = SDA, GP17 = SCL)
const int I2CSDA = 16;
const int I2CSCL = 17;

// Sensor objects
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
Adafruit_BMP3XX bmp;
SFE_UBLOX_GPS gps;

void setup() {
  Serial.begin(9600);
  Wire.setSDA(I2CSDA);
  Wire.setSCL(I2CSCL);
  Wire.begin();

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

  Serial.print("Gyro: ");
  Serial.print(gyro.gyro.x); Serial.print(", ");
  Serial.print(gyro.gyro.y); Serial.print(", ");
  Serial.println(gyro.gyro.z);

  Serial.print("Accel: ");
  Serial.print(accel.acceleration.x); Serial.print(", ");
  Serial.print(accel.acceleration.y); Serial.print(", ");
  Serial.println(accel.acceleration.z);

  // BMP388 Pressure & Altitude
  if (bmp.performReading()) {
    Serial.print("Pressure: ");
    Serial.print(bmp.pressure / 100.0); Serial.print(" hPa\t");
    Serial.print("\nAltitude: ");
    Serial.print(bmp.readAltitude(1013.25)); Serial.println(" m");
  }

  // ZOE-M8Q GPS
  gps.checkUblox(); // Process incoming GPS data

  delay(250);
}