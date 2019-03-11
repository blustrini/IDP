#include <Event.h>
#include <Timer.h>

//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotorR = AFMS.getMotor(1);
Adafruit_DCMotor *myMotorL = AFMS.getMotor(2);
int motorSpeedConst = 205;
int motorSpeedVar = 200;
int motorSpeedFast = 255;
int motorSpeedSlowTurn = 80;
int motorSpeedSlowStraight = 230;
int motorSpeedSlowCorrectLeft = 100;
int delayTime = 10000;

//Motors for pickup wheel
Adafruit_DCMotor *pickupMotor = AFMS.getMotor(3);
int pickupMotorSpeed = 255;

//Pickup wheel timing
#include<Timer.h>
Timer pickupTimer;
bool reversing = false;
unsigned long lastReverseTime;
int reverseDelay = 1200;

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

//Inclusions and variables for right ultrasonic sensors
#include "SR04.h"
//Right
#define TRIG_PIN_R 12
#define ECHO_PIN_R 11
SR04 ultrasoundRight = SR04(ECHO_PIN_R,TRIG_PIN_R);
//Left
#define TRIG_PIN_L 7
#define ECHO_PIN_L 6
SR04 ultrasoundLeft = SR04(ECHO_PIN_L,TRIG_PIN_L);
float actual_dist;

//Switch interrupt pin
const byte switchFrontPin = 2;
const byte switchBackPin = 3;

//TESTTT low and high pins
int low1 = 4;
int high1 = 5;

//Debounce time
int debounceTimeSwitch = 1000;
int debounceTimeHall = 500;
//Last interrupt switches, block detector, hall sensor
static unsigned long lastInterruptTime = 0;
static unsigned long lastInterruptTimeBD = 0;
static unsigned long lastInterruptTimeHall = 0;

//PID variables
float expected_dist = 0;
float last_dist = 0;
float p_gain = 0.4  ;
//float i_gain = 0.005;
float d_gain = 1;
float i_mem = 0;
bool pid_on = false; 
int pid_counter = 0;
int pid_d_counter = 0;
int pid_side;

//Hall detector
int hallDetectPin = 8;
static unsigned long last_detect = 0;
int hall_wait = 1000;

// IR sensor
int analogIRPin = 0;
int IRThreshold = 400; //CALIBRATE THIS
static unsigned long lastIRinterruptTime = 0;
int IRTimeThreshold;

//Motor functions
void MoveForward() {
  myMotorR->setSpeed(motorSpeedConst);
  myMotorR->run(FORWARD);
  myMotorL->setSpeed(motorSpeedVar);
  myMotorL->run(BACKWARD);
}

void MoveBackward() {
  myMotorR->setSpeed(motorSpeedConst);
  myMotorR->run(BACKWARD);
  myMotorL->setSpeed(motorSpeedVar);
  myMotorL->run(FORWARD);
}

void PivotLeft() {
  myMotorL->setSpeed(0);
  myMotorR->setSpeed(motorSpeedFast);
  myMotorR->run(FORWARD);
}

void PivotRight() {
  myMotorL->setSpeed(motorSpeedFast);
  myMotorL->run(BACKWARD);
  myMotorR->setSpeed(0);
}

void MoveStop() {
  pid_on = false;
  myMotorR->setSpeed(0);
  myMotorL->setSpeed(0);
}

void SoftTurnLeft() {
  myMotorR->setSpeed(motorSpeedFast);
  myMotorR->run(FORWARD);
  myMotorL->setSpeed(motorSpeedSlowTurn);
  myMotorL->run(BACKWARD);
}

void SoftTurnRight() {
  myMotorR->setSpeed(motorSpeedSlowTurn);
  myMotorR->run(FORWARD);
  myMotorL->setSpeed(motorSpeedFast);
  myMotorL->run(BACKWARD);
}

void SlightRight() {
  myMotorR->setSpeed(motorSpeedSlowStraight);
  myMotorR->run(FORWARD);
  myMotorL->setSpeed(motorSpeedFast);
  myMotorL->run(BACKWARD);
}

void CorrectLeft() {
  myMotorR->setSpeed(motorSpeedSlowCorrectLeft);
  myMotorR->run(FORWARD);
  myMotorL->setSpeed(motorSpeedFast);
  myMotorL->run(BACKWARD);
}

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

//PID setup function
void PIDSetup(int side) {
  int flusher = 0;
  while (flusher < 100){
    float a = GetUltrasound(side);
    flusher++;
  }
  while (true){
    expected_dist = GetUltrasound(side);
    if (expected_dist > 0 && expected_dist < 200){
      break;
    }
  }
  last_dist = expected_dist;

  pid_on = true;
  pid_side = side;
}

//PID main function
void PID(int side) {
  if (pid_counter % 1 == 0){
    pid_d_counter += 1;
    while (true){
    actual_dist = GetUltrasound(side);
      if (actual_dist < 5*expected_dist) {
        break;
      }
    }
    //PID
    float error_temp = actual_dist - expected_dist;
    //i_mem += i_gain * error_temp;
    i_mem = 0;
    float d_increase = d_gain * (actual_dist - last_dist);
    int motor_increase = (p_gain * error_temp) + i_mem + d_increase;

    //Calculate new motor speed depending on which side of PID
    int newSpeed;
    if (side == 0){
      newSpeed = motorSpeedVar + motor_increase;
    } else{
      newSpeed = motorSpeedVar - motor_increase;
    }
    
    
    //Change variable motor speed 
    if (newSpeed < 255 && newSpeed > 0){
      newSpeed;
    } else if((motorSpeedVar + motor_increase) >= 255){
      motorSpeedVar = 255;
    } else {
      motorSpeedVar = 0;
    }
    myMotorL->setSpeed(motorSpeedVar);
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

//Getting ultrasound data
int GetUltrasound(int side){
  if (side == 0){
    return ultrasoundRight.Distance();
  }else{
    return ultrasoundLeft.Distance();
  }
}

//Stop pid
void PIDStop(){
  pid_on == false;
}

//Switch Servo functions
void ServoAcc(){
  switchServo.write(switchServoPosAcc);
  delay(servoDelay);
}

void ServoRej(){
  switchServo.write(switchServoPosRej);
  delay(servoDelay);
}

void ServoBlock(){
  switchServo.write(switchServoPosBlock);
  delay(servoDelay);
}

/*
//Interrupt routine for hall detector
ISR(PCINT0_vect){
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterruptTimeHall > debounceTimeHall){
    if (digitalRead(hallDetectPin) == HIGH){
      Serial.println(6);
    }
  }
  lastInterruptTimeHall = interruptTime;
}

//Interrupt routine for block detector
ISR(PCINT1_vect){
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterruptTimeBD > debounceTimeSwitch){
    if (digitalRead(A0) == LOW){
      Serial.println(5);
    }
  }
  lastInterruptTimeBD = interruptTime;
}
*/

//Pickup wheel functions
void StartPickupWheel(){
  pickupMotor->setSpeed(pickupMotorSpeed);
  pickupMotor->run(FORWARD);
}

void StopPickupWheel(){
  pickupMotor->setSpeed(0);
}

void ReversePickup(){
  pickupMotor->run(FORWARD);
  reversing = true;
  lastReverseTime = millis();
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

  //low high pins
  pinMode(high1, OUTPUT);
  pinMode(low1, OUTPUT);
  //pinMode(high2, OUTPUT);
  //pinMode(low2, OUTPUT);
  //digitalWrite(low2,LOW);
  //digitalWrite(high2, HIGH);
  digitalWrite(low1,LOW);
  digitalWrite(high1, HIGH);
  
  //Attach Front and Back switch interrupt pins
  pinMode(switchFrontPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchFrontPin), switchFrontSerial, RISING);
  pinMode(switchBackPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchBackPin), switchBackSerial, RISING);

  //Attach servo pins
  blockReleaseServo.attach(9);
  switchServo.attach(10);

  //Declare pin for hall detector
  pinMode(A0, INPUT);

  //Pickup wheel timer
  int wheelReverseEvent = pickupTimer.every(6000, ReversePickup, 0);
  pickupMotor->setSpeed(pickupMotorSpeed);
  pickupMotor->run(BACKWARD);\

  //servo set
  switchServo.write(switchServoPosAcc);
  blockReleaseServo.write(135);
  /*
  //Pin change interrupt for hall detector
  PCMSK1 = B00000001; //Enable A0
  //Block detecting switch
  pinMode(A0, INPUT_PULLUP);
  PCMSK0 = B00000001; //Enable digital pin 8
  PCIFR = B00000000; //Clear all interrupt flags
  PCICR = B00000001; //Enable PCIE0 and PCIE1 group
  */
  
}

void loop() {

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
  const byte i = 9;
  const byte j = 10;
  const byte k = 11;
  const byte l = 12;
  const byte m = 13;
  const byte n = 14;
  const byte o = 15;
  const byte p = 16;
  const byte q = 17;
  const byte r = 18;
  const byte s = 19;
  
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
     PIDSetup(1);
     break;
   case i:
     PIDSetup(0);
     break;
   case j:
     //halt everything
     break;
   case k:
     //resume
     break;
   case l:
     ServoAcc();
     break;
   case m:
     ServoRej();
     break;
   case n:
     ServoBlock();
     break;
   case o:
     CorrectLeft();
     break;
   case p:
     PIDStop();
     break;
   case q:
     StartPickupWheel();
     break;
   case r:
     StopPickupWheel();
     break;
   case s:
     ReleaseBlocks();
     break;
  }
   if (pid_on == true){
    PID(pid_side);
   }
<<<<<<< HEAD


=======
/*
>>>>>>> 29cbdf15de35d93ae81cc602b675aea34aeb82c8
   //Hall detector code
   int HallDetectValue = analogRead(A0);
   if (HallDetectValue > 200){
    if (millis() - last_detect > hall_wait) {
      last_detect = millis();
      Serial.println(6);
    }
   }
<<<<<<< HEAD


=======
*/
>>>>>>> 29cbdf15de35d93ae81cc602b675aea34aeb82c8
   //Update pickup wheel timer
   pickupTimer.update();
   if (reversing == true){
    if (millis() - lastReverseTime > reverseDelay) {
      pickupMotor->run(BACKWARD);
      reversing = false;
    }
   }
  
  /*
   if (analogRead(analogIRPin) > IRThreshold){
    unsigned long IRinterruptTime = millis();
    if ((IRinterruptTime - lastIRinterruptTime) > IRTimeThreshold){
      //send block detected
    }
   }
   */
}
