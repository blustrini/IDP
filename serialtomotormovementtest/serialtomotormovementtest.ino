//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
int motorSpeedFast = 255;

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

void setup() {
  // put your setup code here, to run once:
  //Set up serial port
  AFMS.begin();
  //MoveForward();
  Serial.begin(9600);
  delay(4000);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Read serial
  byte serialInput = Serial.read();
  //Serial.println(serialInput);
  if (serialInput == 255){
    //Serial.println(serialInput);
    //MoveForward();
  }
  if (serialInput == 1){
    Serial.println(serialInput);
    MoveForward();
  }
  else if (serialInput == 2){
    Serial.println(serialInput);
    MoveBackward();
  }
  
}
