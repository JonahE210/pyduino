int redPin = 7;
int greenPin = 8;

void setup() {
  Serial.begin(9600);
  pinMode(greenPin, OUTPUT);
}

void loop() {

  if(Serial.available() > 0){

    String sq = Serial.readString();

    if(sq == "ON"){
      digitalWrite(greenPin, HIGH);
    }
    else if(sq == "OFF"){
      digitalWrite(greenPin, LOW);
    }
    else if(sq == "BLINK"){
      digitalWrite(greenPin, HIGH);
      delay(100);
      digitalWrite(greenPin, LOW);
      delay(100);
      digitalWrite(greenPin, HIGH);
      delay(100);

    }
    else{
      for(int i = 0; i < 5; i++){
        digitalWrite(redPin, HIGH);
        delay(250);
        digitalWrite(redPin, LOW);
        delay(250);
      }
    }
  }



} 