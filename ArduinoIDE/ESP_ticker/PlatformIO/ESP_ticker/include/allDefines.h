#ifndef ALLDEFINES_H
#define ALLDEFINES_H

#define Debug(...)      ({ Serial.print(__VA_ARGS__);         \
                        })

#define Debugln(...)    ({ Serial.println(__VA_ARGS__);       \
                        })

#define Debugf(...)     ({ Serial.printf(__VA_ARGS__);        \
                        })

#define DebugFlush()    ({ Serial.flush(); \
                        })

#define DebugT(...)     ({ _debugBOL(__FUNCTION__, __LINE__);  \
                           Debug(__VA_ARGS__);                 \
                        })

#define DebugTln(...)   ({ _debugBOL(__FUNCTION__, __LINE__);  \
                           Debugln(__VA_ARGS__);        \
                        })

#define DebugTf(...)    ({ _debugBOL(__FUNCTION__, __LINE__);  \
                           Debugf(__VA_ARGS__);                \
                        })

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW

#define MAX_DEVICES  8

#define MAX_SPEED   50

#define CS_PIN      15 // or SS

#define SETTINGS_FILE   "/settings.ini"

#define LOCAL_SIZE      255

#define NEWS_SIZE       512

#define JSON_BUFF_MAX   255

#define MAX_NO_NO_WORDS  20

#define _FW_VERSION "v1.7.3 (04-05-2023)"

#define USE_UPDATE_SERVER

#define _HOSTNAME   "ESPticker"

#define MAX_FILES_IN_LIST   25

#endif // ALLDEFINES_H
