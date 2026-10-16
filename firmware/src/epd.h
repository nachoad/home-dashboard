#pragma once

#include <stddef.h>
#include <stdint.h>

// Driver for the 7.3" Spectra 6 (E6) panel, 800x480, 4 bits per pixel.
// Pixel codes: black 0x0, white 0x1, yellow 0x2, red 0x3, blue 0x5, green 0x6.
// Buffer layout: byte y*400 + x/2, even x in the high nibble.

void epdBegin();
// Sends a full EPD_BUF_SIZE frame and refreshes (~25 s). Buffer may live in PSRAM.
void epdShow(const uint8_t *frame);
void epdClear(uint8_t color);
void epdSleep();
