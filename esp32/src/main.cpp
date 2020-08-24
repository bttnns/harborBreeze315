#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
 
const char *SSID = "";
const char *PWD = "";
 
// Configurables
#define PIN 21
#define NUM_ATTEMPTS 6 // How many times to repeat the code
#define DIP 1 // Remote DIP Switch: 0 or 1

// Delays for keying, should not need to change these (in microseconds)
const int SHORT_DELAY = 380;
const int LONG_DELAY = 770;
const int EXTENDED_DELAY = 8000;

// Harbor breeze remote bits See the manual for the button # mapping
// https://fccid.io/A25-TX012/User-Manual/User-manual-1937614

// Preambles depending on remote DIP position. Code = dpX + func
const char *dp0 = "00000000000000000"; // Dip Switch 0 Preamble
const char *dp1 = "00110000111111101"; // Dip Switch 1 Preamble

// Fan button functions. Button #1 in user manual
// Winter (Counterclockwise)
const char *fw1 = "01110010"; // Fan Speed 1
const char *fw2 = "10110010"; // Fan Speed 2
const char *fw3 = "00110010"; // Fan Speed 3
const char *fw4 = "11010010"; // Fan Speed 4
const char *fw5 = "01010010"; // Fan Speed 5
const char *fw6 = "10010010"; // Fan Speed 6
const char *fwT = "11110010"; //2 Fan ON/OFF
const char *fwN = "00010010"; //3 Nature Breeze

// Summer (Clockwise)
const char *fs1 = "01111010"; // Fan Speed 1
const char *fs2 = "10111010"; // Fan Speed 2
const char *fs3 = "00111010"; // Fan Speed 3
const char *fs4 = "11011010"; // Fan Speed 4
const char *fs5 = "01011010"; // Fan Speed 5
const char *fs6 = "10011010"; // Fan Speed 6
const char *fsT = "11111010"; //2 Fan ON/OFF
const char *fsN = "00011010"; //3 Nature Breeze

// Fan Direction
const char *fwD = "11100010"; //8 Fan Winter Direction
const char *fsD = "11101010"; //8 Fan Summer Direction

// Light button mappings
const char *liH = "00001110"; //4 Home Shield (Lights cycle on for 5-20 minutes and off for 60 minutes, simulating occupancy)
const char *liT = "01101010"; //5 Light ON/OFF
const char *liD = "10101010"; //5 Light DIMMING

// Delay button mappings
const char *deO = "00100010"; //6 Delay Off
const char *de2 = "01101110"; //7 Delay 2H
const char *de4 = "10101110"; //7 Delay 4H
const char *de8 = "00101110"; //8 Delay 8H

// Web server running on port 80
WebServer server(80);
 
// JSON data buffer
StaticJsonDocument<250> jsonDocument;
char buffer[250];
char code[8];

void connectToWiFi() {
  Serial.print("Connecting to ");
  Serial.println(SSID);
  
  WiFi.begin(SSID, PWD);
  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
 
  Serial.print("Connected. IP: ");
  Serial.println(WiFi.localIP());
}

void transmit_char(char *c) {
  if (strcmp(c, "1")) {
    delayMicroseconds(SHORT_DELAY);
    digitalWrite(PIN, HIGH);
    delayMicroseconds(LONG_DELAY);
    digitalWrite(PIN, LOW);
  } else if (strcmp(c, "0")) {
    delayMicroseconds(LONG_DELAY);
    digitalWrite(PIN, HIGH);
    delayMicroseconds(SHORT_DELAY);
    digitalWrite(PIN, LOW);
  }
}

void transmit_code(const char *code) {
  // Transmit a chosen code string using the GPIO transmitter
  for (int t = 0; t < NUM_ATTEMPTS; ++t) {
    // Transmit the preamble first
    if (DIP == 0) {
      for (int n = 0; char c = dp0[n]; ++n) {
        transmit_char(c);
      }
    } else if (DIP == 1) {
      for (int n = 0; char c = dp1[n]; ++n) {
        transmit_char(c);
      }	
    } // Now the function
    for (int n = 0; char c = code[n]; ++n) {
      transmit_char(c);
    }
    digitalWrite(PIN, LOW);
    delayMicroseconds(EXTENDED_DELAY);
  }
}

void build_status(char *status, int error) { 
  jsonDocument.clear(); 
  jsonDocument["status"] = status;
  jsonDocument["error"] = error;
  serializeJson(jsonDocument, buffer);
  Serial.println("Buffer:");
  Serial.println(buffer);  
}

void tx_liT() {
  transmit_code(liT);
  build_status("ok", 0);
  server.send(200, "application/json", buffer);
}

// setup API resources
void setup_routing() {
  server.on("/liT", tx_liT);
 
  // start server
  server.begin();
}

void setup() {
  Serial.begin(9600);
  connectToWiFi();
  setup_routing();  
  pinMode(PIN, OUTPUT);
}
 
void loop() {
  server.handleClient();
}
