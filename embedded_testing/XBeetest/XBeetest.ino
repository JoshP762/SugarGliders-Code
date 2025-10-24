void setup() {
  Serial.begin(9600);       // USB Serial for debugging
  Serial1.setTX(0);         // GP0 = TX to XBee DIN
  Serial1.setRX(1);         // GP1 = RX from XBee DOUT
  Serial1.begin(9600);      // Match XBee's baud rate

  Serial.println("XBee transmitter ready");
}

void loop() {
  Serial1.println("Hello from Pico via XBee!");
  delay(1000); // Send every second
}
