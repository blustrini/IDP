int buttonPin = 2;
int low = 4;
int high = 5;

void setup() {
  pinMode(high, OUTPUT);
  pinMode(low, OUTPUT);
  digitalWrite(low,LOW);
  digitalWrite(high, HIGH);
  pinMode(buttonPin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (digitalRead(buttonPin) == HIGH){
    digitalWrite(LED_BUILTIN, HIGH);
  }
   else {
    digitalWrite(LED_BUILTIN, LOW);
   }
  }
