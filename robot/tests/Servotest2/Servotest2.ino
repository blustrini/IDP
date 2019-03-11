#include <Event.h>
#include <Timer.h>

//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 


//Servo for block release
#include<Servo.h>
Servo blockReleaseServo;
int blockReleaseServoPos = 20; //closed 135 open 20

//Servo for block switch
Servo switchServo;
int switchServoPosAcc = 120;
int switchServoPosRej = 75; //need to be calibrated
int switchServoPosBlock = 40;

//servo delays
int servoDelay = 500;

//Switch interrupt pin
const byte switchFrontPin = 2;
const byte switchBackPin = 3;



//Debounce time
int debounceTimeSwitch = 1000;
int debounceTimeHall = 500;
//Last interrupt switches, block detector, hall sensor
static unsigned long lastInterruptTime = 0;
static unsigned long lastInterruptTimeBD = 0;
static unsigned long lastInterruptTimeHall = 0;


//Serial output functions
void switchFrontSerial() {
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterruptTime > debounceTimeSwitch){
    Serial.println(3);
  }
  lastInterruptTime = interruptTime;
}

void switchBackSerial() {
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterruptTime > debounceTimeSwitch){
    Serial.println(4);
  }
  lastInterruptTime = interruptTime;
}

//Switch Servo functions
void ServoAcc(){
  switchServo.write(switchServoPosAcc);
  Serial.println("Accept");
  delay(servoDelay);
}

void ServoRej(){
  switchServo.write(switchServoPosRej);
  Serial.println("Reject");
  delay(servoDelay);
}

void ServoBlock(){
  switchServo.write(switchServoPosBlock);
  Serial.println("Block");
  delay(servoDelay);
}


//Block Releasing function
void ReleaseBlocks(){
  blockReleaseServo.write(blockReleaseServoPos);
  delay(servoDelay);
}

void setup() {
  // put your setup code here, to run once:

  //Begin Motors
  AFMS.begin();
  
  //Set up serial port
  Serial.begin(9600);
  //delay(1000);
  
  
  //Attach Front and Back switch interrupt pins
  pinMode(switchFrontPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchFrontPin), switchFrontSerial, RISING);
  pinMode(switchBackPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchBackPin), switchBackSerial, RISING);

  //Attach servo pins
  blockReleaseServo.attach(9);
  switchServo.attach(10);
  blockReleaseServo.write(135);
  delay(500);
  switchServo.write(switchServoPosAcc);
  delay(500);

  
}

void loop() {
  int serialInput = 0;

  //Read serial
  while (Serial.available() > 0){
    serialInput += Serial.read();
  }


  if (serialInput > 0){
    Serial.println(serialInput);
  }

  //Switch statement
  const int l = 12;
  const int m = 13;
  const int n = 14;

  switch(serialInput) {
   case l:
     Serial.println(9);
     ServoAcc();
     break;
   case m:
     Serial.println(8);
     ServoRej();
     break;
   case n:
     Serial.println(7);
     ServoBlock();
     break;
  }
}
   
