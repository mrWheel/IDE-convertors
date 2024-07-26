#ifndef RESTAPI_H
#define RESTAPI_H

#include <Arduino.h>

//== Local Headers ==
#include "settingStuff.h"
#include "littlefsStuff.h"
#include "jsonStuff.h"
#include "helperStuff.h"
#include "allDefines.h"

//== Extern Variables ==
extern ESP8266WebServer httpServer;
extern String lastReset;
extern bool Verbose;
extern uint16_t settingLDRhighOffset;
extern uint16_t settingLDRlowOffset;
extern uint8_t settingLocalMaxMsg;
extern uint8_t settingMaxIntensity;
extern uint8_t settingNewsInterval;
extern uint8_t settingNewsMaxMsg;
extern uint8_t settingTextSpeed;
extern uint8_t settingWeerLiveInterval;


//== Function Prototypes ==
void processAPI();
void sendDeviceInfo();
void sendDeviceTime();
void sendDeviceSettings();
void sendLocalMessages();
void sendNewsMessages();
void postMessages();
void postSettings();
void sendApiNotFound(const char *URI);


#endif // RESTAPI_H
