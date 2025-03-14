// PK_konk.ino (Периферийный контроллер)
#define buttonPin 8
#define led1Pin 4  // Ожидание
#define led2Pin 5  // Завершение
#define led3Pin 6  // Запущен
#define BAUD_RATE 9600

bool buttonState = false;
bool lastButtonState = false;
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 50;

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(led3Pin, OUTPUT);
  setLEDs(true, false, false); // Начальное состояние: ожидание
}

void loop() {
  bool reading = !digitalRead(buttonPin); // Инвертируем, так как INPUT_PULLUP

  // Антидребезг
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      
      // Отправка статуса кнопки на КНУ
      Serial.print("B:");
      Serial.print(buttonState ? "1" : "0");
      Serial.println("#");
      
      // Обновление светодиодов
      updateLEDs();
    }
  }
  lastButtonState = reading;
}

void updateLEDs() {
  if (buttonState) {
    setLEDs(false, false, true);  // Процесс запущен (зеленый)
  } else {
    setLEDs(true, false, false);  // Ожидание (красный)
  }
}

void setLEDs(bool led1, bool led2, bool led3) {
  digitalWrite(led1Pin, led1);
  digitalWrite(led2Pin, led2);
  digitalWrite(led3Pin, led3);
}
