#pragma once

// WIFI_SSID, WIFI_PASSWORD and SERVER_URL live in secrets.h (gitignored).
// Copy secrets.example.h to secrets.h and fill it in.
#include "secrets.h"

// Used when the server does not send X-Sleep-Seconds.
#define DEFAULT_SLEEP_S (6UL * 3600UL)
// Retry interval after a WiFi or HTTP failure.
#define RETRY_SLEEP_S   (30UL * 60UL)
// Bounds applied to the server-provided sleep time.
#define MIN_SLEEP_S     (5UL * 60UL)
#define MAX_SLEEP_S     (24UL * 3600UL)

#define WIFI_TIMEOUT_MS 20000
#define HTTP_TIMEOUT_MS 30000

// On USB power the board stays awake (delay instead of deep sleep) so the
// serial port keeps working and it can be reflashed without button presses.
#define STAY_AWAKE_ON_USB 1
