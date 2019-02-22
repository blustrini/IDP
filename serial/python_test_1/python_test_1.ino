
//int buf[2];
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  //delay(1000);
}

// the loop function runs over and over again forever
void loop() {
  byte serialInput=Serial.read();
  Serial.println(serialInput);
  if (serialInput==2){
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(500);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW); // turn the LED off by making the voltage LOW
    delay(500);
  }
}
