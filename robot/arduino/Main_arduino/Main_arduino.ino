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
int debounceTime = 1000;
//Last interrupt
static unsigned long lastInterruptTime = 0;

//PID variables
float expected_dist = 0;
float last_dist = 0;
float p_gain = 0.4  ;
//float i_gain = 0.005;
float d_gain = 1;
//float i_mem = 0;
bool pid_on = false; 
int pid_counter = 0;
int pid_d_counter = 0;

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

void SpinLeft() {
  myMotor1->setSpeed(motorSpeedFast);
  myMotor1->run(FORWARD);
  myMotor2->setSpeed(motorSpeedFast);
  myMotor2->run(FORWARD);
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

//PID setup function
void PIDSetup() {
  int flusher = 0;
  while (flusher < 100){
    float a = sr04.Distance();
    flusher++;
  }
  while (true){
    expected_dist = sr04.Distance();
    if (expected_dist > 0 && expected_dist < 200){
      break;
    }
  }
  last_dist = expected_dist;
}

//PID main function
void pid() {
  if (pid_counter % 1 == 0){
    pid_d_counter += 1;
    while (true){
    actual_dist = sr04.Distance();
      if (actual_dist < 5*expected_dist) {
        break;
      }

    //PID
    float error_temp = actual_dist - expected_dist;
    //i_mem += i_gain * error_temp;
    i_mem = 0;
    float d_increase = d_gain * (actual_dist - last_dist);
    int motor_increase = (p_gain * error_temp) + i_mem + d_increase;

    //Change variable motor speed 
    if ((motorSpeedVar + motor_increase) < 255 && (motorSpeedVar + motor_increase) > 0){
      motorSpeedVar += motor_increase;
    } else if((motorSpeedVar + motor_increase) >= 255){
      motorSpeedVar = 255;
    } else {
      motorSpeedVar = 0;
    }
    myMotorLeft->setSpeed(motorSpeedVar);
    Serial.println(motorSpeedVar);
    //increase counter 
    pid_counter = 0;
    if (pid_d_counter % 10 == 0){
     pid_d_counter = 0;
    last_dist = actual_dist;
    }
  }

  pid_counter += 1;
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
     SpinLeft();
     break;
}
}
