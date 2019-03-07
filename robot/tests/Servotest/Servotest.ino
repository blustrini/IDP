//Servo for block release
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include<Servo.h>
Servo blockReleaseServo;
int servopos = 0; //needs to be calibrated

void setup() {
  // put your setup code here, to run once:
  blockReleaseServo.attach(10);

  
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  blockReleaseServo.write(0);
  delay(1000);
  blockReleaseServo.write(180);
  delay(1000);
  */
  /*
  for (servopos = 0; servopos <=180; servopos +=1){
    blockReleaseServo.write(servopos);
    delay(10);
  }
  for (servopos = 180; servopos >=0 ; servopos -=1){
    blockReleaseServo.write(servopos);
    delay(10);
  }
  */


  blockReleaseServo.write(135);
  delay(500);
  blockReleaseServo.write(20);
  delay(500);

}
