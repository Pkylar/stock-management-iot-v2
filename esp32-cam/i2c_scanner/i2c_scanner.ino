/*
 * I2C Scanner with LED feedback
 * LED blinks to show which pin pair found camera
 * Pattern: long pause, then blink SDA count, pause, blink SCL count
 */
#include <Wire.h>

#define LED_PIN 2

int pinPairs[][2] = {
  {4, 5},    // 0: Freenove
  {40, 39},  // 1: XIAO/Generic
  {17, 18},  // 2: Variant
  {21, 47},  // 3: Variant
  {38, 47},  // 4: Variant
  {4, 41},   // 5: Variant
  {2, 1},    // 6: Variant
};
int numPairs = 7;

void blinkLED(int times, int onMs, int offMs) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, HIGH); delay(onMs);
    digitalWrite(LED_PIN, LOW); delay(offMs);
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  delay(2000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);

  // Try each pin pair
  int foundPair = -1;
  for (int p = 0; p < numPairs; p++) {
    Wire.begin(pinPairs[p][0], pinPairs[p][1]);
    delay(100);
    byte camAddrs[] = {0x21, 0x30, 0x3C, 0x36};
    for (int k = 0; k < 4; k++) {
      Wire.beginTransmission(camAddrs[k]);
      if (Wire.endTransmission() == 0) {
        foundPair = p;
        break;
      }
    }
    Wire.end();
    if (foundPair >= 0) break;
    delay(100);
  }

  if (foundPair >= 0) {
    // SUCCESS: blink pair number + 1 (so pair 0 = 1 blink, pair 1 = 2 blinks, etc)
    // Pattern: 3 fast blinks = found, then pause, then pair number blinks
    blinkLED(3, 100, 100);  // found signal
    delay(1000);
    while(1) {
      blinkLED(foundPair + 1, 500, 500);  // pair number
      delay(3000);
    }
  } else {
    // FAIL: continuous fast blink = nothing found
    while(1) {
      blinkLED(20, 50, 50);
      delay(2000);
    }
  }
}

void loop() {}

