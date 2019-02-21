int buttonPin1 = 2;
int low1 = 4;
int high1 = 5;
int buttonPin2 = 3;
int low2 = 6;
int high2 = 7;

void setup() {
  pinMode(high1, OUTPUT);
  pinMode(low1, OUTPUT);
  pinMode(high2, OUTPUT);
  pinMode(low2, OUTPUT);
  digitalWrite(low2,LOW);
  digitalWrite(high2, HIGH);
  digitalWrite(low1,LOW);
  digitalWrite(high1, HIGH);
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (digitalRead(buttonPin1) == HIGH){
    digitalWrite(LED_BUILTIN, HIGH);
  }
   else {
    digitalWrite(LED_BUILTIN, LOW);
   }
   if (digitalRead(buttonPin2) == HIGH){
    digitalWrite(LED_BUILTIN, HIGH);
  }
   else {
    digitalWrite(LED_BUILTIN, LOW);
   }
  }
