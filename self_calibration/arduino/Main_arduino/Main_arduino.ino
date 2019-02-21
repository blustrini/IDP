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

//TESTTT low and high pins
int low1 = 4;
int high1 = 5;
int low2 = 6;
int high2 = 7;

//Debounce time
int debounceTime = 300;

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
  delay(debounceTime);
  if (digitalRead(switchFrontPin) == HIGH){
    Serial.write("sf");
  }
}

void switchBackSerial() {
  delay(debounceTime);
  if (digitalRead(switchBackPin) == HIGH){
    Serial.write("sb");
  }
}

void setup() {
  // put your setup code here, to run once:

  //Set up serial port
  Serial.begin(9600);
  delay(1000);

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
