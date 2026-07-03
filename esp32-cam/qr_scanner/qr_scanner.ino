/*
 * ESP32-S3 Camera Server
 * Serves JPEG captures via /capture endpoint
 * QR decoding handled by server-side Python script
 */
#include <WiFi.h>
#include <WebServer.h>
#include "esp_camera.h"

const char* ssid = "Tempatkosong";
const char* password = "eskrimmixue";

#define PWDN_GPIO_NUM     -1
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM     15
#define SIOD_GPIO_NUM      4
#define SIOC_GPIO_NUM      5
#define Y9_GPIO_NUM       16
#define Y8_GPIO_NUM       17
#define Y7_GPIO_NUM       18
#define Y6_GPIO_NUM       12
#define Y5_GPIO_NUM       10
#define Y4_GPIO_NUM        8
#define Y3_GPIO_NUM        9
#define Y2_GPIO_NUM       11
#define VSYNC_GPIO_NUM     6
#define HREF_GPIO_NUM      7
#define PCLK_GPIO_NUM     13
#define LED_PIN            2

WebServer server(80);

void handleCapture() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) { server.send(500, "text/plain", "fail"); return; }
  WiFiClient client = server.client();
  String head = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: " + String(fb->len) + "\r\nConnection: close\r\n\r\n";
  client.print(head);
  client.write(fb->buf, fb->len);
  esp_camera_fb_return(fb);
}

void handleRoot() {
  server.send(200, "text/html",
    "<html><body><h2>ESP32-S3 Camera</h2>"
    "<img id='img' style='width:480px'>"
    "<script>function load(){var img=document.getElementById('img');img.onload=function(){setTimeout(load,200)};img.onerror=function(){setTimeout(load,1000)};img.src='/capture?'+Date.now()}; load();</script>"
    "</body></html>");
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.jpeg_quality = 6;
  config.frame_size = FRAMESIZE_QVGA;
  config.fb_count = 2;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.grab_mode = CAMERA_GRAB_LATEST;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("[ERROR] Camera failed");
    while(1) { digitalWrite(LED_PIN, !digitalRead(LED_PIN)); delay(100); }
  }
  Serial.println("[OK] Camera");

  sensor_t *s = esp_camera_sensor_get();
  s->set_brightness(s, 1);
  s->set_contrast(s, 1);
  s->set_sharpness(s, 2);

  WiFi.begin(ssid, password);
  int att = 0;
  while (WiFi.status() != WL_CONNECTED && att < 40) {
    delay(500);
    att++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("[OK] WiFi: " + WiFi.localIP().toString());
    server.on("/", handleRoot);
    server.on("/capture", handleCapture);
    server.begin();
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_PIN, LOW); delay(100);
      digitalWrite(LED_PIN, HIGH); delay(100);
    }
  } else {
    Serial.println("[ERROR] WiFi failed");
    for (int i = 0; i < 5; i++) {
      digitalWrite(LED_PIN, LOW); delay(300);
      digitalWrite(LED_PIN, HIGH); delay(300);
    }
  }
  digitalWrite(LED_PIN, HIGH);
}

unsigned long lastRestart = millis();
const unsigned long RESTART_INTERVAL = 10 * 60 * 1000; // 10 menit

void loop() {
  server.handleClient();
  if (millis() - lastRestart > RESTART_INTERVAL) {
    ESP.restart();
  }
}
