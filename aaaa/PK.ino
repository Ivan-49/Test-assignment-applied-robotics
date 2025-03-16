#define but1 0
#define n 3
#define but 2
#define outP 3
byte leds[] = {9, 10, 11, 3};
bool ledsOn[] = {false, false, false, false};
byte ledsIn[] = {4, 5, 6, 2};
bool ledsInOnLast[] = {true, true, true, true};
bool butInOnLast = true;

void setup() {
  Serial.begin(9600);

  for (byte i = 0; i < n; i++) {
    pinMode(ledsIn[i], INPUT);
  };
  pinMode(ledsIn[n], INPUT_PULLUP);
  for (byte i = 0; i <= n; i++) {
    pinMode(leds[i], OUTPUT);
  };
}


void loop() {

  for (byte i = 0; i < n; i++) {
    if (digitalRead(ledsIn[i]) != ledsInOnLast[i]) {
      if (digitalRead(ledsIn[i])) {
        ledsOn[i] = !ledsOn[i];
      }
      if (ledsOn[i]) {
        analogWrite(leds[i], 2);
      } else {
        analogWrite(leds[i], 0);
      };
      ledsInOnLast[i] = digitalRead(ledsIn[i]);
    }
  };
  
  if (digitalRead(ledsIn[n]) != ledsInOnLast[n]) {
    ledsOn[n] = !ledsOn[n];
    if (ledsOn[n]) {
      digitalWrite(leds[n], HIGH);
    } else {
      digitalWrite(leds[n], LOW);
    };
    ledsInOnLast[n] = digitalRead(ledsIn[n]);
  }
  delay(50);
}
