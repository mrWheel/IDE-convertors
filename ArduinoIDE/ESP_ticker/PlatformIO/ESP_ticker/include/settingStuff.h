#ifndef SETTINGSTUFF_H
#define SETTINGSTUFF_H

#include <Arduino.h>

//== Local Headers ==
#include "ESP_ticker.h"
#include "newsapi_org.h"
#include "helperStuff.h"
#include "allDefines.h"

//== Extern Variables ==
extern uint16_t settingLDRhighOffset;
extern uint16_t settingLDRlowOffset;
extern uint8_t settingLocalMaxMsg;
extern uint8_t settingMaxIntensity;
extern uint8_t settingNewsInterval;
extern uint8_t settingNewsMaxMsg;
extern uint8_t settingTextSpeed;
extern uint8_t settingWeerLiveInterval;


//== Function Prototypes ==
void writeSettings(bool show);
void readSettings(bool show);
void updateSetting(const char *field, const char *newValue);


#endif // SETTINGSTUFF_H
