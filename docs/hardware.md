# Hardware del ESP32-S3-PhotoPainter

Problemas conocidos de la placa: `issues-photopainter.md`. Baterías: `baterias.md`.

## Componentes
- Pantalla: 7.3" E Ink Spectra 6 (E6), 800×480, 6 colores (negro, blanco, amarillo, rojo, azul, verde).
  Refresco completo ~25 s con parpadeo. **Sin refresco parcial/rápido.**
  Datasheet panel: https://files.waveshare.com/wiki/7.3inch-e-Paper-HAT-(E)/7.3inch-e-Paper-(E)-user-manual.pdf
- MCU: ESP32-S3-WROOM-1-N16R8 (16 MB flash QIO, 8 MB PSRAM octal), WiFi 2.4 GHz + BLE 5.
- PMIC: **AXP2101** en Rev 1, **TG28** en Rev 2 (I2C 0x34, IRQ GPIO21, CHGLED GPIO3).
  Librería: XPowersLib (Lewis He); el driver AXP2101 también inicializa el TG28.
- RTC PCF85063, sensor SHTC3 (0x70), codec ES8311 (0x18) + ADC ES7210 (0x40), altavoz, microSD.
- Botones: BOOT=GPIO0 (activo bajo), KEY=GPIO4 (activo bajo), PWR=GPIO5 (activo alto).
- LEDs (activo bajo): rojo GPIO45, verde GPIO42.

## Pines
| Función | GPIO |
|---|---|
| EPD MOSI/SCK/DC/CS/RST/BUSY | 11 / 10 / 8 / 9 / 12 / 13 (BUSY activo bajo) |
| EPD SPI | SPI3_HOST/FSPI, mode 0, CS manual; 4–10 MHz en Arduino, 40 MHz en IDF |
| I2C | SDA=47, SCL=48 |
| SD (SDMMC 4-bit) | CLK=39, CMD=41, D0=40, D1=1, D2=2, D3=38 → `/sdcard` |
| I2S audio | MCLK=14, BCLK=15, WS=16, DOUT=17, DIN=18, PA enable=7 |

## Framebuffer y colores
- 4 bpp, 2 px/byte, 192 000 bytes. Byte `y*400 + x/2`; píxel x par en nibble alto.
- Protocolo con el servidor: `GET /frame.bin?bat=&usb=&boot=&rssi=&key=` → `200` con
  exactamente esos 192 000 bytes (pintar), o `204` (nada nuevo: no tocar el panel). Ambos traen
  `X-Sleep-Seconds` (el firmware lo limita a 5 min–24 h). Cualquier otra cosa → conservar la
  imagen y reintentar en 30 min. `key=1` (despertar por KEY) obliga a responder 200.
  Reservar en PSRAM (`ps_malloc`) y copiar por filas a buffer DRAM antes de SPI (DMA no lee PSRAM).
- Índices: Black=0x0, White=0x1, Yellow=0x2, Red=0x3, Blue=0x5, Green=0x6 (0x4 no se usa).
- RGB "puros" del firmware oficial: negro 0,0,0 · blanco 255,255,255 · amarillo 255,255,0 ·
  rojo 255,0,0 · azul 0,0,255 · verde 0,255,0. Las imágenes deben llegar ya dithered
  (Floyd-Steinberg/Sierra) a esta paleta. tintenklecks usa tintas medidas para mejor resultado.
- Secuencia panel: init `0xAA 49 55 20 08 09 18`, `0x01 3F`, `0x00 5F 69`, `0x61 03 20 01 E0`,
  `0xE3 2F`, `0x04`; datos con `0x10`; refresco `0x04` → `0x12 00` → `0x02 00`; sleep panel `0x07 A5`.

## Alimentación
- USB-C 5 V (alimenta, carga, programa y da logs).
- Batería Li-ion 3.7 V por conector MX1.25 2 pines (Waveshare ofrece 1500 mAh; SKU 32753 = sin batería).
  Esquemático: conector **J2 "PH1.25-2P"**, pin 1 = BAT+ (AXP2101 pin 33), pin 2 = GND.
  Hay otros dos PH1.25-2P, J3 (pila RTC) y H1 (altavoz): no confundirlos.
  AXP2101 carga desde USB-C (500 mA CC, terminación 25 mA). Lectura % con `getBatteryPercent()`.
- Apagar: sin batería basta con quitar el USB; con batería, PWR 5 s. La imagen e-paper se conserva
  sin alimentación; no desconectar durante un refresco.
- Problema conocido (esp32-photoframe, issue Waveshare #5): con USB-C **y** batería conectados a la vez el
  AXP2101 de la Rev 1 puede provocar reinicios. La **Rev 2** (PMIC TG28) lo corrige y conecta el INT
  del RTC al PWRON del PMIC (ver `issues-photopainter.md`). Esquemático v2:
  https://www.waveshare.net/w/upload/a/ae/ESP32-S3-PhotoPainter-Schematic-v2.0.pdf
- Deep sleep ≤ 1 mA según wiki. Para bajar consumo: apagar raíles AXP (ALDO3 codec, ALDO4 panel),
  PA de audio en bajo, desmontar SD, LEDs off, WiFi off antes de `esp_deep_sleep_start()`.
- Timer de deep sleep del ESP32 deriva ~1–3 %; se puede calibrar con el RTC PCF85063.

## Deep sleep con wakeup por timer (patrón oficial)
En arduino-esp32 2.x (PlatformIO `espressif32@6.x`) la función es `esp_sleep_enable_ext1_wakeup`;
`esp_sleep_enable_ext1_wakeup_io` solo existe en ESP-IDF ≥5.3.
```c
esp_sleep_enable_ext1_wakeup_io((1ULL<<GPIO_NUM_0)|(1ULL<<GPIO_NUM_4), ESP_EXT1_WAKEUP_ANY_LOW);
esp_sleep_enable_timer_wakeup(6ULL * 3600 * 1000000ULL); // 6 h
esp_deep_sleep_start();
```
Usar `RTC_DATA_ATTR` para estado entre ciclos; `esp_sleep_get_wakeup_cause()` al arrancar.

## Programación desde macOS
- USB nativo (USB-Serial/JTAG) del ESP32-S3: **no necesita drivers en macOS**; aparece como `/dev/cu.usbmodem*`.
- Auto-download en placa. Modo descarga manual: PWR 5 s (apagar) → mantener BOOT y pulsar PWR.
- Abrir el puerto serie (pyserial, `pio device monitor`) **reinicia la placa** (`rst:0x15 USB_UART_CHIP_RESET`).
- Arduino IDE 2 / arduino-esp32: Board "ESP32S3 Dev Module", USB CDC On Boot: Enabled,
  USB Mode: Hardware CDC and JTAG, Flash QIO 80 MHz 16MB, PSRAM: **OPI PSRAM**,
  Partition: "16M Flash (3MB APP/9.9MB FATFS)" (o Huge APP). Librería: XPowersLib.
- ESP-IDF 5.x (ejemplo oficial requiere ≥5.4 en alguna dependencia): `idf.py set-target esp32s3`,
  `idf.py -p /dev/cu.usbmodemXXXX flash monitor`. sdkconfig: FLASHSIZE_16MB, FLASHMODE_QIO,
  SPIRAM_MODE_OCT, SPIRAM_SPEED_80M.
- Binario fusionado: flashear en offset 0x0 (ESP Launchpad / esptool). Restaurar fábrica: `.bin` de
  `03_Firmware` del repo oficial.

## Notas de una unidad Rev 2
- Placa **Rev 2** (TG28), chip ESP32-S3 rev v0.2, PSRAM AP 8 MB octal (gen 3) a 80 MHz, flash QIO 16 MB.
  PMIC inicializa con el driver AXP2101 (`axp2101: Init PMU SUCCESS!`).
- USB: Espressif "USB JTAG_serial debug unit" (VID 0x303A, PID 0x1001) → `/dev/cu.usbmodem*`.
- Red: en `SERVER_URL` conviene usar la IP fija del servidor en lugar de `.local`; reservar en el
  router las IP del servidor y del marco.
- Firmware de fábrica: **XiaoZhi 2.0.1** (ESP-IDF 5.5.2, `Mode_value: 1` = modo xiaozhi). Arranca en
  modo configuración de red (AP `Xiaozhi-XXXX`, `http://192.168.4.1`) y **no pinta nada**: pantalla en
  blanco es normal. La SD de fábrica trae imágenes de ejemplo en `/sdcard/05_user_ai_img/`.
  SHTC3 responde (ID 0x0887); ES8311/ES7210 inicializan.
- Este firmware: 14 % RAM, 14 % flash; upload ~16 s a 921600 sin pulsar botones (auto-download OK).
  Sin batería `[pmu] battery -1%` (esperado).
- Si el servidor es un Mac, desactivar el reposo del sistema (`pmset sleep 0`).

## Referencias
- Wiki: https://www.waveshare.com/wiki/ESP32-S3-PhotoPainter
- Producto: https://www.waveshare.com/esp32-s3-photopainter.htm?sku=32753
- Repo oficial (ESP-IDF + Arduino): https://github.com/waveshareteam/ESP32-S3-PhotoPainter
  - Pines/PMIC: `04_PowerConsumptionTest/01_Arduino_Src/01_Fac_Test/bsp_config.h`, `bsp_fac.h`
  - Driver EPD: `01_Example/xiaozhi-esp32/components/port_bsp/display_bsp.cpp`
  - Sleep: `01_Example/xiaozhi-esp32/components/user_app_bsp/mode_src/Basic_mode.cpp`
- Esquemático v1: https://files.waveshare.com/wiki/ESP32-S3-PhotoPainter/ESP32-S3-PhotoPainter-Schematic.pdf
  (v2 en la sección Alimentación).
- tintenklecks (Arduino, buen driver EPD + gestión energía): https://github.com/Lissors/tintenklecks
  **Licencia no comercial: no copiar código modificado; usar solo como referencia.**
