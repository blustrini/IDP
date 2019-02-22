//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
int motorSpeedFast = 255;
int motorSpeedSlow = 180;
int delayTime = 10000;

//Switch pins
int switchPinFront = 7;
int switchPinBack = 3;

void runForward() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(FORWARD);
}

void runBackward() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(BACKWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}

void hardLeft() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}

void hardRight() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(BACKWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(FORWARD);
}

void setup() {
  // put your setup code here, to run once:
  AFMS.begin();
  runForward();
}

void loop() {
  //if switch front is pressed, move backwards
  //if (digitalRead(switchPinFront) == HIGH){
    //runBackward();
  //}
  //if switch back switch is pressed, move forward
  //if (digitalRead(switchPinBack) == HIGH){
    //runForward();
  //}
  

}
