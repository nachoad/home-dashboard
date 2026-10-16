// home-dashboard firmware: wake, fetch a pre-dithered 4 bpp frame from the server,
// show it on the e-paper and deep sleep until the next update.

#include <Arduino.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <Wire.h>
#include <driver/rtc_io.h>
#include <esp_sleep.h>

#define XPOWERS_CHIP_AXP2101
#include <XPowersLib.h>

#include "board.h"
#include "config.h"
#include "epd.h"

static XPowersPMU pmu;
static bool pmuOk = false;

RTC_DATA_ATTR static uint32_t bootCount = 0;

static void ledsOff() {
  pinMode(LED_PIN_RED, OUTPUT);
  pinMode(LED_PIN_GREEN, OUTPUT);
  digitalWrite(LED_PIN_RED, HIGH);
  digitalWrite(LED_PIN_GREEN, HIGH);
}

static void powerBegin() {
  pinMode(AUDIO_PA_PIN, OUTPUT);
  digitalWrite(AUDIO_PA_PIN, LOW);

  pmuOk = pmu.begin(Wire, AXP2101_SLAVE_ADDRESS, I2C_PIN_SDA, I2C_PIN_SCL);
  if (!pmuOk) {
    Serial.println("[pmu] AXP2101 not found");
    return;
  }
  // Same rail setup as the official BSP (power_bsp.cpp): DCDC1 + ALDO1-4 at 3.3 V.
  pmu.setDC1Voltage(3300);
  pmu.setALDO1Voltage(3300);
  pmu.setALDO2Voltage(3300);
  pmu.setALDO3Voltage(3300);
  pmu.setALDO4Voltage(3300);
  pmu.enableALDO1();
  pmu.enableALDO2();
  pmu.enableALDO3();
  pmu.enableALDO4();
  pmu.setChargerConstantCurr(XPOWERS_AXP2101_CHG_CUR_500MA);
  pmu.enableBattVoltageMeasure();
  pmu.enableVbusVoltageMeasure();
  delay(50);
}

static int batteryPercent() {
  if (!pmuOk || !pmu.isBatteryConnect()) return -1;
  return pmu.getBatteryPercent();
}

static bool onUsb() {
  return pmuOk && pmu.isVbusIn();
}

static bool connectWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - start > WIFI_TIMEOUT_MS) {
      Serial.println("[wifi] timeout");
      return false;
    }
    delay(200);
  }
  Serial.printf("[wifi] connected, ip=%s rssi=%d\n", WiFi.localIP().toString().c_str(), WiFi.RSSI());
  return true;
}

static void wifiOff() {
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
}

static uint32_t serverSleep(HTTPClient &http) {
  uint32_t sleepS = http.header("X-Sleep-Seconds").toInt();
  if (sleepS == 0) sleepS = DEFAULT_SLEEP_S;
  return constrain(sleepS, MIN_SLEEP_S, MAX_SLEEP_S);
}

// Downloads exactly EPD_BUF_SIZE bytes into frame. Returns the sleep time the
// server asked for (seconds), or 0 on failure. *repaint is false when the
// server answered 204 (nothing new to show).
static uint32_t fetchFrame(uint8_t *frame, bool keyWake, bool *repaint) {
  String url = String(SERVER_URL) + "?bat=" + batteryPercent() + "&usb=" + (onUsb() ? 1 : 0) +
               "&boot=" + bootCount + "&rssi=" + WiFi.RSSI() + "&key=" + (keyWake ? 1 : 0);
  HTTPClient http;
  http.setTimeout(HTTP_TIMEOUT_MS);
  http.begin(url);
  const char *headers[] = {"X-Sleep-Seconds"};
  http.collectHeaders(headers, 1);

  int code = http.GET();
  *repaint = code != HTTP_CODE_NO_CONTENT;
  if (code == HTTP_CODE_NO_CONTENT) {
    Serial.println("[http] 204, keeping current image");
    uint32_t sleepS = serverSleep(http);
    http.end();
    return sleepS;
  }
  if (code != HTTP_CODE_OK) {
    Serial.printf("[http] GET %s -> %d\n", url.c_str(), code);
    http.end();
    return 0;
  }
  int len = http.getSize();
  if (len != EPD_BUF_SIZE) {
    Serial.printf("[http] unexpected length %d\n", len);
    http.end();
    return 0;
  }

  WiFiClient *stream = http.getStreamPtr();
  size_t got = 0;
  uint32_t lastData = millis();
  while (got < EPD_BUF_SIZE && millis() - lastData < HTTP_TIMEOUT_MS) {
    size_t avail = stream->available();
    if (avail) {
      got += stream->readBytes(frame + got, min(avail, (size_t)(EPD_BUF_SIZE - got)));
      lastData = millis();
    } else {
      delay(1);
    }
  }
  uint32_t sleepS = serverSleep(http);
  http.end();

  if (got != EPD_BUF_SIZE) {
    Serial.printf("[http] short read %u\n", (unsigned)got);
    return 0;
  }
  return sleepS;
}

static void goToSleep(uint32_t seconds) {
  Serial.printf("[sleep] %u s\n", (unsigned)seconds);
  Serial.flush();

#if STAY_AWAKE_ON_USB
  if (onUsb()) {
    // Keep USB serial alive; wake early if KEY is pressed.
    uint32_t start = millis();
    while (millis() - start < seconds * 1000UL) {
      if (digitalRead(BTN_PIN_KEY) == LOW) break;
      delay(100);
    }
    ESP.restart();
  }
#endif

  if (pmuOk) {
    // ALDO rails feed the panel, codecs and SD card; DCDC1 (ESP32) stays on.
    pmu.disableALDO1();
    pmu.disableALDO2();
    pmu.disableALDO3();
    pmu.disableALDO4();
  }
  gpio_hold_en((gpio_num_t)AUDIO_PA_PIN);

  esp_sleep_enable_ext1_wakeup(1ULL << BTN_PIN_KEY, ESP_EXT1_WAKEUP_ANY_LOW);
  rtc_gpio_pulldown_dis((gpio_num_t)BTN_PIN_KEY);
  rtc_gpio_pullup_en((gpio_num_t)BTN_PIN_KEY);
  esp_sleep_enable_timer_wakeup((uint64_t)seconds * 1000000ULL);
  esp_deep_sleep_start();
}

void setup() {
  Serial.begin(115200);
  delay(200);
  bootCount++;
  gpio_hold_dis((gpio_num_t)AUDIO_PA_PIN);
  pinMode(BTN_PIN_KEY, INPUT_PULLUP);
  ledsOff();

  esp_sleep_wakeup_cause_t cause = esp_sleep_get_wakeup_cause();
  // Pressing KEY always forces a repaint.
  bool keyWake = cause == ESP_SLEEP_WAKEUP_EXT1;
  Serial.printf("[boot] #%u wake cause %d\n", (unsigned)bootCount, cause);
  powerBegin();
  Serial.printf("[pmu] battery %d%% usb=%d\n", batteryPercent(), onUsb());

  uint8_t *frame = (uint8_t *)ps_malloc(EPD_BUF_SIZE);
  if (!frame) {
    Serial.println("[mem] PSRAM alloc failed");
    goToSleep(RETRY_SLEEP_S);
  }

  uint32_t sleepS = 0;
  bool repaint = true;
  digitalWrite(LED_PIN_GREEN, LOW);
  if (connectWifi()) sleepS = fetchFrame(frame, keyWake, &repaint);
  wifiOff();
  digitalWrite(LED_PIN_GREEN, HIGH);

  if (sleepS == 0) {
    // Keep the last image on screen and try again later.
    digitalWrite(LED_PIN_RED, LOW);
    delay(500);
    digitalWrite(LED_PIN_RED, HIGH);
    goToSleep(RETRY_SLEEP_S);
  }
  if (!repaint) {
    free(frame);
    goToSleep(sleepS);
  }

  epdBegin();
  epdShow(frame);
  epdSleep();
  free(frame);
  goToSleep(sleepS);
}

void loop() {}
