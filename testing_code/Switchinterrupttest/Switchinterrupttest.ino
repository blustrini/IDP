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

//Button state
//bool buttonState = true;

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
  //Set up serial port
  Serial.begin(9600);
  delay(1000);

  
  //Attach Front and Back switch interrupt pins
  pinMode(switchFrontPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchFrontPin), switchFrontSerial, RISING);
  pinMode(switchBackPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchBackPin), switchBackSerial, RISING);
  
}

void loop() {
  // put your main code here, to run repeatedly:

}
