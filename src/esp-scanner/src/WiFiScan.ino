/*
 *  This sketch demonstrates how to scan WiFi networks. 
 *  The API is almost the same as with the WiFi Shield library, 
 *  the most obvious difference being the different file you need to include:
 */
#include "ESP8266WiFi.h"

int oblast = 0;

void setup() {
  Serial.begin(115200);

  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
}

void loop() {
  // WiFi.scanNetworks will return the number of networks found
  while (Serial.available()){
    char command = Serial.read();
    if (command == 'p'){
      Serial.print("wifi");
      Serial.print('@');
    }
    else if (command == 'u'){
      int n = WiFi.scanNetworks();
      if (n > 0){
        for (int i = 0; i < n; ++i){
          Serial.print(WiFi.BSSIDstr(i));
          Serial.print(";");
          Serial.print(WiFi.RSSI(i)+100); 
          Serial.print("\n");
          if (i == n-1){
            Serial.print('@');
          }
        }
      }
    }
  }
  //Serial.println("");

  // Wait a bit before scanning again
  delay(50);
}
