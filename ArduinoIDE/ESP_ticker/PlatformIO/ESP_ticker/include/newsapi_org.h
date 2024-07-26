#ifndef NEWSAPI_ORG_H
#define NEWSAPI_ORG_H

#include <Arduino.h>

//== Local Headers ==
#include "ESP_ticker.h"
#include "littlefsStuff.h"
#include "helperStuff.h"
#include "allDefines.h"

//== Extern Variables ==
extern uint8_t settingNewsMaxMsg;


//== Function Prototypes ==
bool getNewsapiData();
void removeNewsData();


#endif // NEWSAPI_ORG_H
