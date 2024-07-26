/* 
***************************************************************************  
**  Program  : Debug.h, part of ESP_tickerExtend
**
**  Copyright (c) 2021 Willem Aandewiel
**  Met dank aan Erik
**
**  TERMS OF USE: MIT License. See bottom of file.                                                            
***************************************************************************      
*/
#ifndef DEBUG_H
#define DEBUG_H

/*---- start macro's ------------------------------------------------------------------*/

//-- moved to allDefines.h // #define Debug(...)      ({ Serial.print(__VA_ARGS__);         \
//-- moved to allDefines.h //                         })
//-- moved to allDefines.h // #define Debugln(...)    ({ Serial.println(__VA_ARGS__);       \
//-- moved to allDefines.h //                         })
//-- moved to allDefines.h // #define Debugf(...)     ({ Serial.printf(__VA_ARGS__);        \
//-- moved to allDefines.h //                         })

//-- moved to allDefines.h // #define DebugFlush()    ({ Serial.flush(); \
//-- moved to allDefines.h //                         })


//-- moved to allDefines.h // #define DebugT(...)     ({ _debugBOL(__FUNCTION__, __LINE__);  \
//-- moved to allDefines.h //                            Debug(__VA_ARGS__);                 \
//-- moved to allDefines.h //                         })
//-- moved to allDefines.h // #define DebugTln(...)   ({ _debugBOL(__FUNCTION__, __LINE__);  \
//-- moved to allDefines.h //                            Debugln(__VA_ARGS__);        \
//-- moved to allDefines.h //                         })
//-- moved to allDefines.h // #define DebugTf(...)    ({ _debugBOL(__FUNCTION__, __LINE__);  \
//-- moved to allDefines.h //                            Debugf(__VA_ARGS__);                \
//-- moved to allDefines.h //                         })

/*---- einde macro's ------------------------------------------------------------------*/

char _bol[128];
void _debugBOL(const char *fn, int line)
{
   
  snprintf(_bol, sizeof(_bol), "[%02d:%02d:%02d][%7u|%6u] %-12.12s(%4d): ", \
                hour(), minute(), second(), \
                ESP.getFreeHeap(), ESP.getMaxFreeBlockSize(),\
                fn, line);
                 
  Serial.print (_bol);
}

/***************************************************************************
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the
* "Software"), to deal in the Software without restriction, including
* without limitation the rights to use, copy, modify, merge, publish,
* distribute, sublicense, and/or sell copies of the Software, and to permit
* persons to whom the Software is furnished to do so, subject to the
* following conditions:
*
* The above copyright notice and this permission notice shall be included
* in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
* OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
* IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
* CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
* OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
* THE USE OR OTHER DEALINGS IN THE SOFTWARE.
* 
****************************************************************************
*/

#endif  //  DEBUG_H