//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotorRight = AFMS.getMotor(1);
Adafruit_DCMotor *myMotorLeft = AFMS.getMotor(2);
int motorSpeedFast = 255;
int motorSpeedSlowTurn = 80;
int motorSpeedSlowStraight = 210;
int delayTime = 10000;

//Switch interrupt pin
const byte switchFrontPin = 2;
const byte switchBackPin = 3;

//TESTTT low and high pins
int low1 = 4;
int high1 = 5;
int low2 = 6;
int high2 = 7;

//Debounce time
int debounceTime = 1000;
//Last interrupt
static unsigned long lastInterruptTime = 0;

//Motor functions
void MoveForward() {
  myMotorRight->setSpeed(motorSpeedFast);
  myMotorRight->run(FORWARD);
  myMotorLeft->setSpeed(motorSpeedFast);
  myMotorLeft->run(BACKWARD);
}

void MoveBackward() {
  myMotorRight->setSpeed(motorSpeedFast);
  myMotorRight->run(BACKWARD);
  myMotorLeft->setSpeed(motorSpeedFast);
  myMotorLeft->run(FORWARD);
}

void PivotLeft() {
  myMotorLeft->setSpeed(0);
  myMotorRight->setSpeed(motorSpeedFast);
  myMotorRight->run(FORWARD);
}

void PivotRight() {
  myMotorLeft->setSpeed(motorSpeedFast);
  myMotorLeft->run(BACKWARD);
  myMotorRight->setSpeed(0);
}

void MoveStop() {
  myMotorRight->setSpeed(0);
  myMotorLeft->setSpeed(0);
}

void SoftTurnLeft() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedSlowTurn);
  myMotor2->run(BACKWARD);
}

void SoftTurnRight() {
  myMotorRight->setSpeed(motorSpeedSlowTurn);
  myMotorRight->run(FORWARD);
  myMotorLeft->setSpeed(motorSpeedFast);
  myMotorLeft->run(BACKWARD);
}

void SlightRight() {
  myMotorRight->setSpeed(motorSpeedSlowStraight);
  myMotorRight->run(FORWARD);
  myMotorLeft->setSpeed(motorSpeedFast);
  myMotorLeft->run(BACKWARD);
}

//Serial output functions
void switchFrontSerial() {
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterruptTime > debounceTime){
    Serial.println(3);
  }
  lastInterruptTime = interruptTime;
}

void switchBackSerial() {
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterruptTime > debounceTime){
    Serial.println(4);
  }
  lastInterruptTime = interruptTime;
}

void setup() {
  // put your setup code here, to run once:

  //Begin Motors
  AFMS.begin();
  
  //Set up serial port
  Serial.begin(9600);
  //delay(1000);

  //low high pins
  pinMode(high1, OUTPUT);
  pinMode(low1, OUTPUT);
  pinMode(high2, OUTPUT);
  pinMode(low2, OUTPUT);
  digitalWrite(low2,LOW);
  digitalWrite(high2, HIGH);
  digitalWrite(low1,LOW);
  digitalWrite(high1, HIGH);
  
  //Attach Front and Back switch interrupt pins
  pinMode(switchFrontPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchFrontPin), switchFrontSerial, RISING);
  pinMode(switchBackPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchBackPin), switchBackSerial, RISING);
  
}

void loop() {
  //Write serial based on sensor output
  
  //Read serial
  byte serialInput = Serial.read();

  //Switch statement
  const byte a = 1;
  const byte b = 2;
  const byte c = 3;
  const byte d = 4;
  const byte e = 5;
  const byte f = 6;
  const byte g = 7;
  const byte h = 8;
  
  switch(serialInput) {
   case a:
     MoveForward();
     break;
   case b:
     MoveBackward();
     break;
   case c:
     PivotLeft();
     break;
   case d:
     PivotRight();
     break;
   case e:
     MoveStop();
     break;
   case f:
     SoftTurnLeft();
     break;
   case g:
     SoftTurnRight();
     break;
   case h:
     SlightRight();
     break;
}
}
