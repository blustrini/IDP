//collects data from an analog sensor

int sensorpin = 1;                 // analog pin used to connect the sharp sensor
int val = 0;                 // variable to store the values from sensor(initially zero)

void setup()
{
  Serial.begin(9600);               // starts the serial monitor
  pinMode(5,OUTPUT);
}
 
void loop()
{
  val = analogRead(A1);       // reads the value of the sharp sensor
  Serial.println(val); // prints the value of the sensor to the serial monitor
  if (val > 475){
    digitalWrite(5,LOW);
  }
  else{
    digitalWrite(5,HIGH);
  }
}
