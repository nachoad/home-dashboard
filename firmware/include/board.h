#pragma once

// Pin map from waveshareteam/ESP32-S3-PhotoPainter (bsp_config.h, user_app.cpp).

// E-paper (SPI, CS driven by hand)
#define EPD_PIN_MOSI 11
#define EPD_PIN_SCK  10
#define EPD_PIN_DC   8
#define EPD_PIN_CS   9
#define EPD_PIN_RST  12
#define EPD_PIN_BUSY 13  // low while busy

// I2C (AXP2101 PMIC 0x34, SHTC3 0x70, PCF85063, codecs)
#define I2C_PIN_SDA 47
#define I2C_PIN_SCL 48

// Buttons
#define BTN_PIN_BOOT 0  // active low
#define BTN_PIN_KEY  4  // active low, used as deep-sleep wake button

// LEDs (active low)
#define LED_PIN_RED   45
#define LED_PIN_GREEN 42

// Audio amplifier enable, kept low so the speaker draws nothing
#define AUDIO_PA_PIN 7

#define EPD_WIDTH    800
#define EPD_HEIGHT   480
#define EPD_BUF_SIZE (EPD_WIDTH * EPD_HEIGHT / 2)  // 4 bpp -> 192000 bytes
