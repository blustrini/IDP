//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);

void setup() {
  // put your setup code here, to run once:
  AFMS.begin();
  myMotor1->setSpeed(255);
  myMotor1->run(BACKWARD);
}

void loop() {
  // put your main code here, to run repeatedly:

}
