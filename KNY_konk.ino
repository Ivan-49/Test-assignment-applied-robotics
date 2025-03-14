// KNY_konk.ino (Контроллер нижнего уровня)
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h> // Для реализации UDP (пример для ESP8266)

#define RX_PIN 10
#define TX_PIN 11
#define BAUD_RATE 9600
#define UDP_PORT 5005

SoftwareSerial pcSerial(RX_PIN, TX_PIN);
WiFiUDP udp;

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";
const char* kvuIP = "192.168.1.100"; // IP КВУ

void setup() {
  Serial.begin(BAUD_RATE);
  pcSerial.begin(BAUD_RATE);
  
  // Подключение к Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  udp.begin(UDP_PORT);
}

void loop() {
  // Прием данных от ПК
  if (pcSerial.available()) {
    String data = pcSerial.readStringUntil('#');
    data.trim();
    
    if (data.startsWith("B:")) {
      // Отправка данных на КВУ по UDP
      udp.beginPacket(kvuIP, UDP_PORT);
      udp.print(data + "#");
      udp.endPacket();
      Serial.println("Sent to KVU: " + data);
    }
  }

  // Прием команд от КВУ (если требуется)
  int packetSize = udp.parsePacket();
  if (packetSize) {
    char buffer[64];
    int len = udp.read(buffer, sizeof(buffer)-1);
    buffer[len] = 0;
    Serial.print("Received from KVU: ");
    Serial.println(buffer);
  }
}
