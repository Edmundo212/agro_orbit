#include <HTTPClient.h>
#include <WiFi.h>
#include <math.h>

const char *WIFI_SSID = "Wokwi-GUEST";
const char *WIFI_PASSWORD = "";
const char *API_URL = "http://host.wokwi.internal:8000/api/iot/lectura";

const unsigned long SEND_INTERVAL_MS = 5000;
unsigned long lastSend = 0;

void connectWiFi() {
  Serial.print("Conectando a Wokwi-GUEST");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD, 6);

  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("WiFi conectado. IP: ");
  Serial.println(WiFi.localIP());
}

void sendReading() {
  const float seconds = millis() / 1000.0f;
  const float humidity =
      constrain(48.0f + 16.0f * sinf(seconds / 17.0f) + random(-30, 31) / 10.0f,
                15.0f, 85.0f);
  const float temperature =
      constrain(21.0f + 4.0f * sinf(seconds / 23.0f + 1.0f) +
                    random(-15, 16) / 10.0f,
                10.0f, 35.0f);
  const float ph =
      constrain(6.5f + 0.45f * sinf(seconds / 31.0f) + random(-10, 11) / 100.0f,
                4.0f, 9.0f);

  char body[160];
  snprintf(body, sizeof(body),
           "{\"dispositivo\":\"wokwi-esp32-01\","
           "\"humedad_suelo\":%.1f,\"temperatura\":%.1f,\"ph\":%.2f}",
           humidity, temperature, ph);

  WiFiClient client;
  HTTPClient http;
  if (!http.begin(client, API_URL)) {
    Serial.println("No se pudo iniciar la conexión HTTP.");
    return;
  }

  http.addHeader("Content-Type", "application/json");
  const int status = http.POST(body);
  Serial.printf("POST %s -> HTTP %d | %s\n", API_URL, status, body);

  if (status > 0) {
    Serial.println(http.getString());
  } else {
    Serial.printf("Error HTTP: %s\n", http.errorToString(status).c_str());
  }

  http.end();
}

void setup() {
  Serial.begin(115200);
  randomSeed(esp_random());
  connectWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  const unsigned long now = millis();
  if (now - lastSend >= SEND_INTERVAL_MS) {
    lastSend = now;
    sendReading();
  }

  delay(50);
}
