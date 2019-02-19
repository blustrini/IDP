int buttonPin = 7;

void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  reading = digitalRead(buttonPin);

  if (reading == HIGH){
    digitalWrite(LED_BUILTIN, HIGH);
  }
}
