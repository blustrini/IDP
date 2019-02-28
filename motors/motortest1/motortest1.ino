//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
int motorSpeedFast = 255;
int motorSpeedSlowTurn = 80;
int motorSpeedSlowStraight = 210;
int spinDelay = 1000;
int pivotDelay = 4650;

//Motor functions
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
  myMotor2->setSpeed(0);
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
}

void PivotRight() {
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
  myMotor1->setSpeed(0);
}

void MoveStop() {
  myMotor1->setSpeed(0);
  myMotor2->setSpeed(0);
}

void SoftTurnLeft() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedSlowTurn);
  myMotor2->run(BACKWARD);
}

void SoftTurnRight() {
  myMotor1->setSpeed(motorSpeedSlowTurn);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}

void SlightRight() {
  myMotor1->setSpeed(motorSpeedSlowStraight);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}


void setup() {
  // put your setup code here, to run once:
  AFMS.begin();
  Serial.begin(9600);
  
}

void loop() {
  /*
  delay(5000);
  MoveForward();
  delay(5000);
  MoveBackward();
  delay(600);
  PivotLeft();
  delay(2300);
  MoveBackward();
  delay(2000);
  SoftTurnLeft();
  delay(3200);
  MoveBackward();
  */

  delay(5000);
  SlightRight();
  delay(2000);
  MoveBackward();
  delay(200);
  SoftTurnLeft();
  delay(500);
  MoveForward();
  delay(2000);
  
}
