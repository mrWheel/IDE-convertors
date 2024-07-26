#ifndef LITTLEFSSTUFF_H
#define LITTLEFSSTUFF_H

#include <Arduino.h>

//== Local Headers ==
#include "allDefines.h"

//== Extern Variables ==
extern uint32_t nrReboots;
extern uint8_t settingLocalMaxMsg;


//== Function Prototypes ==
void readLastStatus();
void writeLastStatus();
bool readFileById(const char* fType, uint8_t mId);
bool writeFileById(const char* fType, uint8_t mId, const char *msg);
void updateMessage(const char *field, const char *newValue);
void writeToLog(const char *logLine);


#endif // LITTLEFSSTUFF_H
