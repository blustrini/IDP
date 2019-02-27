//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
int motorSpeedFast = 255;
int motorSpeedSlow = 200;
int spinDelay = 1000;
int pivotDelay = 4650;

void MoveForward() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}

void MoveBackward() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(BACKWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(FORWARD);
}

void PivotLeft() {
  myMotor1->setSpeed(0);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(FORWARD);
}

void PivotRight() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(BACKWARD);
  myMotor2->setSpeed(0);
}

void SpinLeft() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(BACKWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}

void MoveStop() {
  myMotor1->setSpeed(0);
  myMotor2->setSpeed(0);
}

void SoftTurn() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedSlow);
  myMotor2->run(BACKWARD);
}

void SlightRight() {
  myMotor1->setSpeed(motorSpeedSlow);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}

void setup() {
  // put your setup code here, to run once:
  AFMS.begin();
  delay(5000);
  SlightRight();
}

void loop() {
 
  
}
