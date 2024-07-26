#ifndef FSEXPLORER_H
#define FSEXPLORER_H

#include <Arduino.h>

//== Local Headers ==
#include "helperStuff.h"
#include "ESP_ticker.h"
#include "sendIndexPage.h"
#include "restAPI.h"
#include "allDefines.h"

//== Extern Variables ==
extern ESP8266WebServer httpServer;
extern bool Verbose;


//== Function Prototypes ==
void setupFSexplorer();
void APIlistFiles();
bool handleFile(String&& path);
void handleFileUpload();
void formatLittleFS();
const String formatBytes(size_t const& bytes);
bool freeSpace(uint16_t const& printsize);
void updateFirmware();
void reBootESP();
void doRedirect(String msg, int wait, const char* URL, bool reboot);


#endif // FSEXPLORER_H
