#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
int motorSpeed = 255;
int motorSpeedSlow = 180;
int delayTime = 10000;

void setup() {
  // put your setup code here, to run once:
  AFMS.begin();
  myMotor1->setSpeed(motorSpeed);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeed);
  myMotor2->run(BACKWARD);
}

void loop() {
  delay(delayTime);
  myMotor1->run(BACKWARD);
  myMotor2->run(FORWARD);
  delay(delayTime);
  myMotor1->run(FORWARD);
  myMotor2->run(BACKWARD);
  delay(delayTime);
  myMotor1->setSpeed(motorSpeedSlow);
  myMotor1->run(FORWARD);
  myMotor2->run(BACKWARD);
  // put your main code here, to run repeatedly:

}
