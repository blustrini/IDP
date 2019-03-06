//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotorR = AFMS.getMotor(1);
Adafruit_DCMotor *myMotorL = AFMS.getMotor(2);
int motorSpeedConst = 200;
int motorSpeedVar = 200;
int motorSpeedFast = 255;
int motorSpeedSlowTurn = 80;
int motorSpeedSlowStraight = 230;
int delayTime = 10000;

//Motors for pickup wheel and block release mechanism
Adafruit_DCMotor *pickupMotor = AFMS.getMotor(3);
Adafruit_DCMotor *releaseMotor = AFMS.getMotor(4);
int pickupMotorSpeed = 150;
int releaseMotorSpeed = 50;

//Inclusions and variables for right ultrasonic sensors
#include "SR04.h"
//Right
#define TRIG_PIN_R 12
#define ECHO_PIN_R 11
SR04 ultrasoundRight = SR04(ECHO_PIN_R,TRIG_PIN_R);
//Left
#define TRIG_PIN_L 10
#define ECHO_PIN_L 9
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

//Variables for block handling
//block detect pin is A0
int hallDetectPin = 8;
int servoPin = 7;
#include <Servo.h>
Servo myServo;
int servoPosAcc = 0;
int servoPosRej = 40; //need to be calibrated
int servoPosBlock = 90;

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

//Servo functions
void ServoAcc(){
  myServo.write(servoPosAcc);
}

void ServoRej(){
  myServo.write(servoPosRej);
}

void ServoBlock(){
  myServo.write(servoPosBlock);
}

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
    if (digitalRead(A0) == HIGH){
      Serial.println(5);
    }
  }
  lastInterruptTimeBD = interruptTime;
}

//Pickup wheel functions
void StartPickupWheel(){
  pickupMotor->setSpeed(pickupMotorSpeed);
  pickupMotor->run(FORWARD);
}

void StopPickupWheel(){
  pickupMotor->setSpeed(0);
}

//Block Releasing function
void ReleaseBlocks(){
  releaseMotor->setSpeed(releaseMotorSpeed);
  releaseMotor->run(FORWARD);
  //add delay then stop motor? DELETE IF NECESSARY
  delay(1);
  releaseMotor->setSpeed(0);
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

  //Attach servo pin
  myServo.attach(servoPin);

  //Declare pin for hall detector
  pinMode(hallDetectPin, INPUT);
  //Pin change interrupt for hall detector
  PCMSK0 = B00000001; //Enable digital pin 8
  //Block detecting switch
  pinMode(A0, INPUT_PULLUP);
  PCMSK1 = B00000001; //Enable analogue pin A0
  PCIFR = B00000000; //Clear all interrupt flags
  PCICR = B00000011; //Enable PCIE0 and PCIE1 group
  
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
     SlightRight();
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
}
