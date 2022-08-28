unsigned long time;
int sensorVal;

void setup() {
    Serial.begin(9600);
}

void loop() {
  
  time = millis();
  sensorVal = analogRead(A0);

  Serial.print(time);
  Serial.print(",");
  Serial.println(sensorVal);

  delay(2000);

}
