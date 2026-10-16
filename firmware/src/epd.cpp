#include "epd.h"

#include <Arduino.h>
#include <SPI.h>

#include "board.h"

// Command sequence follows Waveshare's 7.3inch e-Paper (E) reference driver (EPD_7in3e).

static SPIClass epdSpi(FSPI);
static const SPISettings kSpiSettings(10000000, MSBFIRST, SPI_MODE0);

static void waitIdle() {
  uint32_t start = millis();
  while (digitalRead(EPD_PIN_BUSY) == LOW) {
    if (millis() - start > 60000) {
      Serial.println("[epd] busy timeout");
      return;
    }
    delay(10);
  }
}

static void sendCommand(uint8_t cmd) {
  digitalWrite(EPD_PIN_DC, LOW);
  digitalWrite(EPD_PIN_CS, LOW);
  epdSpi.beginTransaction(kSpiSettings);
  epdSpi.transfer(cmd);
  epdSpi.endTransaction();
  digitalWrite(EPD_PIN_CS, HIGH);
}

static void sendData(const uint8_t *data, size_t len) {
  digitalWrite(EPD_PIN_DC, HIGH);
  digitalWrite(EPD_PIN_CS, LOW);
  epdSpi.beginTransaction(kSpiSettings);
  for (size_t i = 0; i < len; i++) epdSpi.transfer(data[i]);
  epdSpi.endTransaction();
  digitalWrite(EPD_PIN_CS, HIGH);
}

static void command(uint8_t cmd, std::initializer_list<uint8_t> data) {
  sendCommand(cmd);
  for (uint8_t b : data) sendData(&b, 1);
}

static void reset() {
  digitalWrite(EPD_PIN_RST, HIGH);
  delay(20);
  digitalWrite(EPD_PIN_RST, LOW);
  delay(2);
  digitalWrite(EPD_PIN_RST, HIGH);
  delay(20);
}

static void panelInit() {
  reset();
  waitIdle();
  delay(30);
  command(0xAA, {0x49, 0x55, 0x20, 0x08, 0x09, 0x18});
  command(0x01, {0x3F});
  command(0x00, {0x5F, 0x69});
  command(0x03, {0x00, 0x54, 0x00, 0x44});
  command(0x05, {0x40, 0x1F, 0x1F, 0x2C});
  command(0x06, {0x6F, 0x1F, 0x17, 0x49});
  command(0x08, {0x6F, 0x1F, 0x1F, 0x22});
  command(0x30, {0x03});
  command(0x50, {0x3F});
  command(0x60, {0x02, 0x00});
  command(0x61, {0x03, 0x20, 0x01, 0xE0});  // 800 x 480
  command(0x84, {0x01});
  command(0xE3, {0x2F});
  sendCommand(0x04);  // power on
  waitIdle();
}

static void refresh() {
  sendCommand(0x04);
  waitIdle();
  command(0x06, {0x6F, 0x1F, 0x17, 0x49});
  command(0x12, {0x00});  // display refresh
  waitIdle();
  command(0x02, {0x00});  // power off
  waitIdle();
}

void epdBegin() {
  pinMode(EPD_PIN_CS, OUTPUT);
  pinMode(EPD_PIN_DC, OUTPUT);
  pinMode(EPD_PIN_RST, OUTPUT);
  pinMode(EPD_PIN_BUSY, INPUT);
  digitalWrite(EPD_PIN_CS, HIGH);
  epdSpi.begin(EPD_PIN_SCK, -1, EPD_PIN_MOSI, -1);
  panelInit();
}

void epdShow(const uint8_t *frame) {
  // SPI must not read PSRAM directly; copy one row at a time through DRAM.
  static uint8_t row[EPD_WIDTH / 2];
  sendCommand(0x10);
  for (int y = 0; y < EPD_HEIGHT; y++) {
    memcpy(row, frame + y * sizeof(row), sizeof(row));
    sendData(row, sizeof(row));
  }
  refresh();
}

void epdClear(uint8_t color) {
  static uint8_t row[EPD_WIDTH / 2];
  memset(row, (color << 4) | color, sizeof(row));
  sendCommand(0x10);
  for (int y = 0; y < EPD_HEIGHT; y++) sendData(row, sizeof(row));
  refresh();
}

void epdSleep() {
  command(0x07, {0xA5});
}
