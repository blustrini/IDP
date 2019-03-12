
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int serialInput = 0;

  //Read serial
  while (Serial.available() > 0){
    serialInput = Serial.read();
  }
  
  if (serialInput > 0){
    Serial.println(serialInput);
  }
  
}
