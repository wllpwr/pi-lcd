/*
  This example connects to an unencrypted WiFi network.
  Then it prints the MAC address of the board,
  the IP address obtained, and other network details.

  created 13 July 2010
  by dlf (Metodo2 srl)
  modified 31 May 2012
  by Tom Igoe
*/
#include <SPI.h>
#include <WiFiNINA.h>


#include "arduino_secrets.h"
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID (name)
int status = WL_IDLE_STATUS;     // the WiFi radio's status

const uint16_t port = 9999;
const char * host = "100.64.3.3";
int rep = 0;

WiFiClient client;

void setup() {
  Serial.begin(9600);

  status = WiFi.begin(ssid);
  if ( status != WL_CONNECTED) {
    Serial.println("Couldn't connect to WiFi...");
  }
  else {
    Serial.println("Connected to WiFi!");
    Serial.println("\nStarting connection...");
  }
}

void loop() {
  if (client.connect(host, port)) {
      Serial.println("Connected to server...");
      // Make a HTTP request:
      client.print(rep);
      delay(5000);
      rep++; 
      
    }
   else {
    Serial.println("Couldn't establish connection to server...");
    // try again after 10 seconds
    delay(10000);
   }
}
