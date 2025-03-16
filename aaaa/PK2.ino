#define n 3
#define but 8
byte leds[] = {4, 5, 6};
bool ledsOn[] = {false, false, false};
bool ledsIn = false;
bool lastButtonState = false;
String inChar = "";

void setup() {
  Serial.begin(9600);

  pinMode(but, INPUT_PULLUP);
  for (byte i = 0; i < n; i++) {
    pinMode(leds[i], OUTPUT);
  }
}


void loop() {
  
  if (!digitalRead(but) != lastButtonState) {
    ledsIn = digitalRead(but);
    Serial.println("B:" + String(ledsIn) + "#");
    lastButtonState = !digitalRead(but);
  }
  while (Serial.available() > 0) {
    inChar = Serial.readString();
    if (inChar[0] == 'l') {
      // l:1;1;1#
      for (byte i = 0; i < n; i++) {
        if ((inChar[2 + i * 2] == '1') != ledsOn[i]) {
          digitalWrite(leds[i], HIGH);
          ledsOn[i] = !ledsOn[i];
        };
      }
      for (byte i = 0; i < n; i++) {
        digitalWrite(leds[i], LOW);
      }
    };
  }
  delay(50);
}

