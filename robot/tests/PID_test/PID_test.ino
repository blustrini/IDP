
//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotorRight = AFMS.getMotor(1);
Adafruit_DCMotor *myMotorLeft = AFMS.getMotor(2);
int motorSpeedVar = 200;
int motorSpeedConst = 200;

//Inclusions and variables for ultrasonic sensor
#include "SR04.h"
#define TRIG_PIN 12
#define ECHO_PIN 11
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
float actual_dist;

//PID variables
float expected_dist = 15;
float p_gain = 2;
float i_gain = 2;
float i_mem = 0;

//Counter
int counter = 0;

//Motor functions
void MoveForward() {
  myMotorRight->setSpeed(motorSpeedConst);
  myMotorRight->run(FORWARD);
  myMotorLeft->setSpeed(motorSpeedVar);
  myMotorLeft->run(BACKWARD);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  AFMS.begin();
  delay(2000);
  MoveForward();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (counter % 5 == 0){
    actual_dist = sr04.Distance();
    //Serial.print(dist);
    //Serial.println("cm");

    //PID
    float error_temp = actual_dist - expected_dist;
    i_mem += i_gain * error_temp;
    int motor_increase = (p_gain * error_temp) + i_mem;

    //Change variable motor speed 
    if (motorSpeedVar < 255 && motorSpeedVar > 0){
      motorSpeedVar += motor_increase;
      myMotorLeft->setSpeed(motorSpeedVar);
    }
    //increase counter 
    counter = 0;
  }

  counter += 1;
 

}
