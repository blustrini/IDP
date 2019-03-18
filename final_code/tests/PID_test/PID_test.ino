
//Inclusions and variables for Motor
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotorRight = AFMS.getMotor(1);
Adafruit_DCMotor *myMotorLeft = AFMS.getMotor(2);
int motorSpeedVar = 150;
int motorSpeedConst = 150;

//Inclusions and variables for ultrasonic sensor
#include "SR04.h"
#define TRIG_PIN 12
#define ECHO_PIN 11
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
float actual_dist;

//PID variables
float expected_dist = 0;
float last_dist = 0;
float p_gain = 0.4  ;
float i_gain = 0.005;
float d_gain = 1;
float i_mem = 0;

//Counter
int counter = 0;
int d_counter = 0;

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
  Serial.print("expected_dist:");
  Serial.println(expected_dist);
  last_dist = expected_dist;
}

void loop() {
  // put your main code here, to run repeatedly:

  if (counter % 1 == 0){
    d_counter += 1;
    while (true){
    actual_dist = sr04.Distance();
      if (actual_dist < 5*expected_dist) {
        break;
      }
    }
    Serial.print(actual_dist);
    Serial.println("cm");
    Serial.print("Derivative: ");
    Serial.print(actual_dist-last_dist);
    Serial.println("cm");

    //PID
    float error_temp = actual_dist - expected_dist;
    //Serial.println(p_gain* error_temp);
    //Serial.println(
    //i_mem += i_gain * error_temp;
    i_mem = 0;
    float d_increase = d_gain * (actual_dist - last_dist);
    int motor_increase = (p_gain * error_temp) + i_mem + d_increase;
    Serial.print("Imem ");
    Serial.println(i_mem);
    Serial.print("Pmotorincrease ");
    Serial.println(p_gain * error_temp);
    Serial.print("Dmotorincrease ");
    Serial.println(d_increase);
    Serial.println(motor_increase);

    //Change variable motor speed 
    if ((motorSpeedVar + motor_increase) < 255 && (motorSpeedVar + motor_increase) > 0){
      motorSpeedVar += motor_increase;
    } else if((motorSpeedVar + motor_increase) >= 255){
      motorSpeedVar = 255;
      Serial.println("OVER");
    } else {
      motorSpeedVar = 0;
      Serial.println("UNDER");
    }
    myMotorLeft->setSpeed(motorSpeedVar);
    Serial.println(motorSpeedVar);
    //increase counter 
    counter = 0;
    if (d_counter % 10 == 0){
     d_counter = 0;
    last_dist = actual_dist;
    }
  }

  counter += 1;
 
  
}
