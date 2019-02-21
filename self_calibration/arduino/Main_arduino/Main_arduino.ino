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

//Switch interrupt pin
const byte switchFrontPin = 2;
const byte switchBackPin = 3;
                     
//Motor functions
void MoveForward() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(FORWARD);
}

void MoveBackward() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(BACKWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}

void HardLeft() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(BACKWARD);
}

void HardRight() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(BACKWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(FORWARD);
}

void MoveStop() {
  myMotor1->setSpeed(0);
  myMotor2->setSpeed(0);
}

//Serial output functions
void switchFrontSerial() {
  Serial.println("sf");
}

void switchBackSerial() {
  Serial.println("sb");
}

void setup() {
  // put your setup code here, to run once:

  //Set up serial port
  Serial.begin(9600);
  delay(1000);

  //Attach Front and Back switch interrupt pins
  pinMode(switchFrontPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchFrontPin), switchFrontSerial, RISING);
  pinMode(switchBackPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchBackPin), switchBackSerial, RISING);
  
}

void loop() {
  //Write serial based on sensor output
  
  //Read serial
  int serialInput = Serial.read();

  //Switch statement
  switch(serialInput) {
   case '1':
     MoveForward();
     break;
   case '2':
     MoveBackward();
     break;
   case '3':
     HardLeft();
     break;
   case '4':
     HardRight();
     break;
   case '5':
     MoveStop();
     break;
}
}
