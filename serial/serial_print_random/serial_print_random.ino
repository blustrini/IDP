int x;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
  x = 1;
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(x);
  if (x == 100) {
    x = 0;
  }
  x += 1;
  delay(500);
}
