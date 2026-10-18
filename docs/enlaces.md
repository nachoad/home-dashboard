# Enlaces de documentación e implementación

## Índice: todo lo que trata del ESP32-S3-PhotoPainter
| Tema | Enlace | Detalle |
|---|---|---|
| Wiki oficial | https://www.waveshare.com/wiki/ESP32-S3-PhotoPainter | Specs, flasheo, FAQ |
| Producto | https://www.waveshare.com/esp32-s3-photopainter.htm | Precio, opción con batería |
| Repo oficial | https://github.com/waveshareteam/ESP32-S3-PhotoPainter | Ejemplos ESP-IDF/Arduino, firmware de fábrica |
| Issues cerrados | https://github.com/waveshareteam/ESP32-S3-PhotoPainter/issues?q=is%3Aissue+state%3Aclosed | Resumen: `docs/issues-photopainter.md` |
| Esquemático Rev 1 (AXP2101) | https://files.waveshare.com/wiki/ESP32-S3-PhotoPainter/ESP32-S3-PhotoPainter-Schematic.pdf | Batería J2: pin 1 = +, pin 2 = GND |
| Esquemático Rev 2 (TG28) | https://www.waveshare.net/w/upload/a/ae/ESP32-S3-PhotoPainter-Schematic-v2.0.pdf | INT del RTC → PWRON |
| Repo del demo original | https://github.com/wurongmin/ESP32-S3-PhotoPainter | |
| Firmware tintenklecks | https://github.com/Lissors/tintenklecks | Arduino; licencia no comercial |
| Firmware esp32-photoframe | https://github.com/aitjcize/esp32-photoframe | ESP-IDF, flasher web, paleta medida |
| Firmware nginx + Home Assistant | https://hackaday.io/project/205124-esp32-wifi-e-ink-photo-frame | Arduino, MQTT, JPEG en el ESP32 |
| Blog de Charlie Molthrop | https://charliemolthrop.com/blog/esp32-photopainter | Modelo de color, conversión a BMP 6 colores, carga por SD/WiFi, uso como cliente de voz |
| Baterías compatibles | `docs/baterias.md` | Conector 1.25 mm, polaridad, candidatas |
| Precio y alternativas | `docs/pantallas-epaper.md` | Precio final en España con envío |
| Marcos 3D para imprimir | https://www.printables.com/model/1783831-waveshare-e-ink-esp32-s3-photopainter-frame?lang=es | Printables |

El detalle de cada enlace está en las secciones de abajo.

## Waveshare ESP32-S3-PhotoPainter (hardware de este proyecto)
- Wiki oficial (specs, flasheo, FAQ, firmware de fábrica): https://www.waveshare.com/wiki/ESP32-S3-PhotoPainter
- Página de producto: https://www.waveshare.com/esp32-s3-photopainter.htm
- Repo oficial (ESP-IDF + ejemplos Arduino): https://github.com/waveshareteam/ESP32-S3-PhotoPainter
  - Pines y PMIC (Arduino): `04_PowerConsumptionTest/01_Arduino_Src/01_Fac_Test/bsp_config.h`, `bsp_fac.h`
  - Driver del panel: `01_Example/xiaozhi-esp32/components/port_bsp/display_bsp.cpp`
  - Deep sleep / timer: `01_Example/xiaozhi-esp32/components/user_app_bsp/mode_src/Basic_mode.cpp`
  - Firmware de fábrica para restaurar: `03_Firmware`
- Issues cerrados (resumen en `docs/issues-photopainter.md`): https://github.com/waveshareteam/ESP32-S3-PhotoPainter/issues?q=is%3Aissue+state%3Aclosed
- Esquemático Rev 2 (PMIC TG28): https://www.waveshare.net/w/upload/a/ae/ESP32-S3-PhotoPainter-Schematic-v2.0.pdf
- Repo del demo original: https://github.com/wurongmin/ESP32-S3-PhotoPainter
- Demo en zip: https://files.waveshare.com/wiki/ESP32-S3-PhotoPainter/ESP32-S3-PhotoPainter-Demo.zip
- Esquemático: https://files.waveshare.com/wiki/ESP32-S3-PhotoPainter/ESP32-S3-PhotoPainter-Schematic.pdf
  (batería: J2 PH1.25-2P, pin 1 = BAT+, pin 2 = GND; ver `docs/baterias.md`)
- LiPo con PicoBlade 1.25 mm (The Pi Hut, 150/500/1200 mAh): https://thepihut.com/products/1200mah-3-7v-lipo-battery-1-25mm-picoblade-connector
- Manual del panel 7.3" e-Paper (E): https://files.waveshare.com/wiki/7.3inch-e-Paper-HAT-(E)/7.3inch-e-Paper-(E)-user-manual.pdf
- Blog de Charlie Molthrop, "The ESP32-S3 PhotoPainter: Six-Color E-Paper Imaging and Voice-AI Conversion"
  (2026-06-04): https://charliemolthrop.com/blog/esp32-photopainter. Paleta Spectra 6, dithering y BMP de
  800×480 (1.152.054 bytes), carga por microSD (`06_user_Foundation_img`) o WiFi (AP, `192.168.4.1`),
  USB solo CDC/JTAG (sin almacenamiento masivo), firmware XiaoZhi y su uso como cliente de voz. No trae
  datos de batería ni de consumo. Conversor: https://www.val.town/x/dcm31/epaper-photo
- E-Paper API (drivers de Waveshare): https://www.waveshare.com/wiki/E-Paper_API_Analysis
- Dithering Floyd-Steinberg (guía Waveshare): https://www.waveshare.com/wiki/E-Paper_Floyd-Steinberg
- Conversor a 6 colores (Windows/macOS): https://files.waveshare.com/wiki/common/ConverTo6c_bmp-7.3.zip
- Marcos 3D para imprimir (Printables, "Waveshare E-Ink ESP32-S3 PhotoPainter Frame"):
  https://www.printables.com/model/1783831-waveshare-e-ink-esp32-s3-photopainter-frame?lang=es

## Proyectos de referencia
- **tintenklecks** — firmware Arduino para el PhotoPainter: driver EPD, AXP2101, deep sleep con
  calibración por RTC, web UI con dithering en el navegador. Licencia no comercial (solo referencia).
  https://github.com/Lissors/tintenklecks
- **PhotoPainter-Nginx-Home-Assistant-Device** (will-rigby, Hackaday) — firmware Arduino para el
  PhotoPainter: despierta cada 30 min, descarga una imagen aleatoria de un **nginx** por HTTP a la SD,
  la decodifica en el propio ESP32 (JPEG con JPEGDEC, o BMP; PNG no por falta de RAM), recorta para
  llenar la pantalla y aplica Floyd-Steinberg a 6 colores. Cada 5 min publica temperatura, humedad
  (SHTC3) y voltaje de batería por **MQTT con autodiscovery de Home Assistant**. Licencia no indicada
  en Hackaday.
  https://hackaday.io/project/205124-esp32-wifi-e-ink-photo-frame
  Repo: https://github.com/will-rigby/PhotoPainter-Nginx-Home-Assistant-Device · Vídeo: https://www.youtube.com/watch?v=A8poN4a6Aiw
- **RPiZeroW-ePaper-Display** — servidor en Rust para Raspberry Pi Zero W + Waveshare 7.3" Spectra 6
  (driver EPD7IN3E): descarga una imagen por URL, dither Floyd-Steinberg a 6 colores, refresco
  programado por franjas horarias (`config.json`), web UI en el puerto 8888, servicio systemd.
  Sin batería (siempre enchufado). Licencia CC BY-NC-SA 4.0.
  https://github.com/bolausson/RPiZeroW-ePaper-Display
- **InkyPi** — dashboard e-ink para Raspberry Pi (4, 3, Zero 2 W) en Python + Flask, con web UI y
  plugins (imagen, periódico/cómic, reloj, IA, tiempo, calendario Google/Outlook/Apple) y playlists
  programadas. Soporta Pimoroni Inky Impression (4"–13.3") e Inky wHAT, y Waveshare Spectra 6
  (4", 7.3", 13.3") y B/N vía `waveshare_epd`. Licencia GPL 3.0 (reutilizable).
  Docs: `docs/installation.md`, `docs/building_plugins.md`, `docs/troubleshooting.md`.
  https://github.com/fatihak/InkyPi
- **doorplate-diy** (Data and Operations LLC) — letrero e-ink de sala de reuniones con ESP32: un
  Mac con Flask y panel de control (`/status`, `/update`, Docker opcional); el ESP32 despierta cada
  15 min, pide el estado por HTTP, repinta y vuelve a deep sleep (mismo esquema que este proyecto).
  Python, licencia MIT.
  https://github.com/dataandops/doorplate-diy
- **esp32-photoframe** (aitjcize) — firmware ESP-IDF alternativo que soporta el PhotoPainter
  (`waveshare_photopainter_73`, objetivo por defecto). Web UI en `photoframe.local`, API REST,
  rotación desde la SD o por **URL (HTTP pull a un servidor, con ETag/304)**, dithering
  Floyd-Steinberg con **paleta medida y calibración** del panel, deep sleep (~10 µA según el
  README), integración con Home Assistant. Imágenes en la SD (la flash está ocupada por OTA).
  Flasher web (Chrome/Edge): https://aitjcize.github.io/esp32-photoframe/#flash
  Licencia: GitHub dice MIT, pero el README remite a la del ejemplo de Waveshare.
  - Web (demo + flasher): https://aitjcize.github.io/esp32-photoframe/
  - Repo: https://github.com/aitjcize/esp32-photoframe
  - Protocolo de URL rotation: https://github.com/aitjcize/esp32-photoframe/blob/main/docs/API.md
  - Paleta medida: https://github.com/aitjcize/esp32-photoframe/blob/main/docs/MEASURED_PALETTE.md
  - Servidor de imágenes (Google Photos, Immich, tiempo...): https://github.com/aitjcize/esp32-photoframe-server
  - Conversor CLI/npm: https://github.com/aitjcize/epaper-image-convert
  - Aviso: el AXP2101 provoca reinicios con USB-C y batería conectados a la vez
    (https://github.com/waveshareteam/ESP32-S3-PhotoPainter/issues/5#issuecomment-3876269519).

## Pimoroni Inky Impression
- Guía de inicio: https://learn.pimoroni.com/article/getting-started-with-inky-impression
- Librería Python: https://github.com/pimoroni/inky
- Esquemático 7.3" Spectra: https://cdn.shopify.com/s/files/1/0174/1800/files/inky_impression_73_spectra_schematic.pdf?v=1745854872
- Esquemático 13.3" Spectra: https://cdn.shopify.com/s/files/1/0174/1800/files/inky_impression_133_spectra_schematic.pdf?v=1745855925
- Marco imprimible en 3D "Inky Impression 2025 Edition 7.3" Frame" (MakerWorld; detalles sin
  verificar, la web bloquea la descarga automática):
  https://makerworld.com/es/models/1482862-inky-impression-2025-edition-7-3-frame#profileId-1548643

## Toolchain y librerías
- PlatformIO: https://docs.platformio.org/
- arduino-esp32: https://docs.espressif.com/projects/arduino-esp32/en/latest/
- ESP-IDF deep sleep: https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/system/sleep_modes.html
- USB-Serial/JTAG del ESP32-S3: https://docs.espressif.com/projects/esp-iot-solution/en/latest/usb/usb_overview/usb_serial_jtag.html
- ESP Launchpad (flasheo desde el navegador): https://espressif.github.io/esp-launchpad/
- XPowersLib (AXP2101): https://github.com/lewisxhe/XPowersLib
- Pillow (servidor): https://pillow.readthedocs.io/
- Open-Meteo API (tiempo, sin clave): https://open-meteo.com/en/docs
- Claude API, PDFs y salida estructurada: https://docs.claude.com/en/docs/build-with-claude/pdf-support
- Google Calendar API (Python quickstart): https://developers.google.com/workspace/calendar/api/quickstart/python
