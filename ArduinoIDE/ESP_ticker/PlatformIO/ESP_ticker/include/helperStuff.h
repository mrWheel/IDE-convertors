#ifndef HELPERSTUFF_H
#define HELPERSTUFF_H

#include <Arduino.h>

//== Local Headers ==
#include "littlefsStuff.h"
#include "allDefines.h"

//== Extern Variables ==

//== Function Prototypes ==
bool compare(String x, String y);
bool isNumericp(const char *timeStamp, int8_t len);
int8_t splitString(String inStrng, char delimiter, String wOut[], uint8_t maxWords);
void strConcat(char *dest, int maxLen, const char *src);
void strConcat(char *dest, int maxLen, float v, int dec);
void strConcat(char *dest, int maxLen, int v);
void strToLower(char *src);
void strCopy(char *dest, int maxLen, const char *src, int frm, int to);
void strCopy(char *dest, int maxLen, const char *src);
void strLTrim(char *dest, int maxLen, const char tChar );
void strRTrim(char *dest, int maxLen, const char tChar );
void strTrim(char *dest, int maxLen, const char tChar );
void strRemoveAll(char *dest, int maxLen, const char tChar);
void strTrimCntr(char *dest, int maxLen);
int strIndex(const char *haystack, const char *needle, int start);
int strIndex(const char *haystack, const char *needle);
int stricmp(const char *a, const char *b);
float formatFloat(float v, int dec);
float strToFloat(const char *s, int dec);
void parseJsonKey(const char *sIn, const char *key, char *val, int valLen);
uint8_t utf8Ascii(uint8_t ascii);
void utf8Ascii(char* s);
void getRevisionData();


#endif // HELPERSTUFF_H
