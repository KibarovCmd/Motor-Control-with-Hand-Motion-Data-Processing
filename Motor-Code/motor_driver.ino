#include <Servo.h>

Servo sg90; 

size_t received_data;
int data;


int bytesToInt(uint8_t *bytes, size_t length) {
  int result = 0;

  for (size_t i = 0; i < length; i++) {
    result += (bytes[i] - '0') * pow(10, length - 1 - i);
  }

  return result;
}

void setup() {
  Serial.begin(9600);
  sg90.attach(9);
}

void loop() {
  if (Serial.available() > 0) {
    char buffer[3];
    received_data = Serial.readBytesUntil('\n', (uint8_t*)buffer, 3);
    data = bytesToInt(buffer, received_data);

    if (data > 240) data = 240;
    if (data < 30) data = 30;

    data = map(data, 30, 240, 0, 180);
    if(data > 0 && data <= 30) sg90.write(0);
    if(data > 30 && data <= 60) sg90.write(30);
    if(data > 60 && data <= 90) sg90.write(45);
    if(data > 90 && data <= 120) sg90.write(90);
    if(data > 120 && data <= 150) sg90.write(135);
    if(data > 150 && data <= 180) sg90.write(180);
    //Serial.println(data);
  }
}
