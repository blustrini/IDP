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
//Last interrupt
static unsigned long lastInterruptTime = 0;

//Serial output functions
void switchFrontSerial() {
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterruptTime > debounceTime){
    Serial.write("sf");
  }
  lastInterruptTime = interruptTime;
}

void switchBackSerial() {
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterruptTime > debounceTime){
    Serial.write("sb");
  }
  lastInterruptTime = interruptTime;
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
  // put your main code here, to run repeatedly:

}
